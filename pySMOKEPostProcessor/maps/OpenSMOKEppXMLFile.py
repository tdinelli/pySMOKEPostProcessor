'''
MODULE: OpenSMOKEppXMLFile
@Authors:
    Alberto Cuoci [1], Timoteo Dinelli[1]
    [1]: CRECK Modeling Lab, Department of Chemistry, Materials, and Chemical Engineering, Politecnico di Milano
@Contacts:
    alberto.cuoci@polimi.it
    timoteo.dinelli@polimi.it
@Additional notes:
    This code is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
    Please report any bug to: alberto.cuoci@polimi.it
    This is a modified class frome the original one OpenSMOKEppXMLFile.py inside PyTools4OpenSMOKE 
    modified by Timoteo Dinelli in order to perform post processing analysis for gas phase simulations
'''

import os
import xml.etree.ElementTree as ET
import numpy as np
import re
import pandas as pd
import sys
from scipy import interpolate

from pySMOKEPostProcessor.maps.KineticMap import KineticMap

class OpenSMOKEppXMLFile:

    '''
    Description of the OpenSMOKEppXMLFile class
    TODO
    '''
    
    def __init__(self, OutputFolder: str, kineticFolder: str):
    
        kin = KineticMap(kineticFolder)
        xml_file_name = os.path.join(OutputFolder, 'Output.xml')

        tree = ET.parse(xml_file_name)
        root = tree.getroot()
        
        # System type
        systemType = ((root.find('Type')).text).strip()
        if (systemType != "HomogeneousReactor" and 
            systemType != "Flamelet" and 
            systemType != "Flame1D" and 
            systemType != "Flame2D"):

            if(systemType == "BatchReactor" or 
               systemType == "PlugFlowReactor" or 
               systemType == "PerfectlyStirredReactor"):
            
                print(" * WARNING: You are running an older version of OpenSMOKE++ that is no longer mantained!\n",
                      "          Some of the functions in this class may not work!")
            
            else:
                sys.exit(f"Unknown system type: {systemType}")
        
        # Check simulation/kinetics consistency
        dummy = root.find('mass-fractions')
        dummy = (dummy.text).split()
        list_names = []
        column_index_of_massfractions_profiles = []
        for i in range(int(dummy[0])):
            list_names.append(dummy[1+i*3])
            column_index_of_massfractions_profiles.append(int(dummy[3+i*3]))
        if (len(list_names) != kin.NumberOfSpecies):
            sys.exit("The kinetic mechanism is not consistent with the simulation")
        for i in range(kin.NumberOfSpecies):
            if (list_names[i] != kin.species[i]):
                sys.exit("The kinetic mechanism is not consistent with the simulation")
        
        # Recover additional variables
        dummy = root.find('additional')
        dummy = (dummy.text).split('\n')
        dummy = [i for i in dummy if not i.isnumeric() and i != '']
        n_additional = len(dummy)
        additional_variable = [i.split()[0] + ' ' + i.split()[1] for i in dummy]
        index = [int(i.split()[-1]) for i in dummy]
        add_var_idx = index
        for i in range(len(additional_variable)):
            if ('temperature' in additional_variable[i]):      index_T = index[i] - 2
            if ('pressure' in additional_variable[i]):         index_P = index[i] - 2
            if ('mol-weight' in additional_variable[i]):       index_mw = index[i] - 2
            if ('density' in additional_variable[i]):          index_rho = index[i] - 2
            if ('heat-release' in additional_variable[i]):     index_Q = index[i] - 2
            if ('csi' in additional_variable[i]):              index_csi = index[i] - 2
            if ('mixture-fraction' in additional_variable[i]): index_csi = index[i] - 2
            if ('axial-coordinate' in additional_variable[i]): index_csi = index[i] - 2
            if ('x-coord' in additional_variable[i]):          index_x   = index[i] - 2
            if ('y-coord' in additional_variable[i]):          index_y   = index[i] - 2
            if ('z-coord' in additional_variable[i]):          index_z   = index[i] - 2
            if ('fvSoot' in additional_variable[i]):           index_fv  = index[i] - 2
        
        # Read profiles
        profiles_size = root.find('profiles-size')
        profiles_size = (profiles_size.text).split()
        npts = int(profiles_size[0])
        nc = n_additional + kin.NumberOfSpecies

        profiles = root.find('profiles')
        profiles = (profiles.text).split()
        profiles = np.reshape(profiles, (npts,nc))
        profiles = np.float32(profiles)
        
        # Extract relevant profiles
        time = profiles[:, 0]
        T = profiles[:,index_T]
        P = profiles[:,index_P]
        mw = profiles[:,index_mw]
        rho = profiles[:,index_rho]
        x_coord = profiles[:, index_x]
        y_coord = profiles[:, index_y]
        z_coord = profiles[:, index_z]
        fvSOOT = profiles[:, index_fv]
       
        #Q = profiles[:,index_Q]
        
        if (systemType == 'Flame1D'):
            csi = profiles[:,index_csi]
        elif (systemType == 'Flamelet'):
            csi = [1]*npts - profiles[:,index_csi]
        else:
            csi = [0]*npts
        
        # Composition
        Y = profiles[:,-kin.NumberOfSpecies:]
        X = Y*mw.reshape(-1,1)/np.transpose(kin.mws.reshape(-1,1))
        
        # Additional variables name
        for i in range(len(column_index_of_massfractions_profiles)):
            if(Y[0, column_index_of_massfractions_profiles[i] - len(additional_variable)] > 1e-8): # Warning this can generate bugs
                additional_variable.append('conversion-' + list_names[i]) 

        # Assign internal members
        
        self.npts = npts
        self.ns = kin.NumberOfSpecies
        self.nc = nc

        self.time = time
        self.T = T
        self.P = P
        self.mw = mw
        self.rho = rho
        #self.Q = Q
        self.csi = csi
        
        if (systemType == 'Flame1D'):
            self.csi = csi

        if (systemType == 'Flame2D'):
            self.csi = csi
        
        if (systemType == 'Flamelet'):
            self.csi = csi

        self.Y = Y
        self.X = X

        self.additional_variable = additional_variable
        self.add_var_idx = add_var_idx
        self.kin = kin
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.z_coord = z_coord
        self.fvSOOT  = fvSOOT
    def getProfile(self, name: str):

        if ('time' in name):
            return self.time
        elif ('temperature' in name):
            return self.T
        elif ('pressure' in name):
            return self.P
        elif ('mol-weight' in name):
            return self.mw
        elif ('density' in name):
            return self.rho
        elif ('heat-release' in name):
            return 'self.Q'
        elif ('csi' in name):
            return self.csi
        elif ('mixture-fraction' in name):
            return self.csi
        elif ('axial-coordinate' in name):
            return self.csi
        else:
            if ('conversion' in name):
                raise Exception(f'{name} is not supported yet')
            else:
                raise Exception(f'{name} is not supported yet')

    def getProfileXY(self, name: str, nameY: str):
        if ('time' in name):
            XX = self.time
        elif ('temperature' in name):
            XX = self.T
        elif ('pressure' in name):
            XX = self.P
        elif ('mol-weight' in name):
            XX = self.mw
        elif ('density' in name):
            XX = self.rho
        elif ('heat-release' in name):
            XX = 'self.Q'
        elif ('csi' in name):
            XX = self.csi
        elif ('mixture-fraction' in name):
            XX = self.csi
        elif ('axial-coordinate' in name):
            XX = self.csi
        elif ('x-coord' in name):
            XX = self.x_coord
        elif ('y-coord' in name):
            XX = self.y_coord
        elif ('z-coord' in name):
            XX = self.z_coord
        else:
            if ('conversion' in name):
                raise Exception(f'{name} is not supported yet')
            else:
                raise Exception(f'{name} is not supported yet')

        idx_spec = self.kin.IndexFromSpeciesName(nameY)

        if ('fvSOOT' in nameY):
            Xsel = self.fvSOOT
        else:
            idx_spec = self.kin.IndexFromSpeciesName(nameY)
            Xsel = self.X[:,idx_spec]

        return XX, Xsel

