# ---------------------------------------------------------------------------------- #
#                                                                                    #
#                              _____  __  ___ ____   __ __  ______                   #
#                ____   __  __/ ___/ /  |/  // __ \ / //_/ / ____/____   ____        #
#               / __ \ / / / /\__ \ / /|_/ // / / // ,<   / __/  / __ \ / __ \       #
#              / /_/ // /_/ /___/ // /  / // /_/ // /| | / /___ / /_/ // /_/ /       #
#             / .___/ \__, //____//_/  /_/ \____//_/ |_|/_____// .___// .___/        #
#            /_/     /____/                                   /_/    /_/             #
#                                                                                    #
#                                                                                    #
# ---------------------------------------------------------------------------------- #
# Please refer to the copyright statement and license                                #
# information at the end of this file.                                               #
# ---------------------------------------------------------------------------------- #
#                                                                                    #
#         Authors: Timoteo Dinelli     <timoteo.dinelli@polimi.it>                   #
#                  Luna Pratali Maffei <luna.pratali@polimi.it>                      #
#                  Edoardo Ramalli     <edoardo.ramalli@polimi.it>                   #
#                  Andrea Nobili       <edoardo.ramalli@polimi.it>                   #
#                                                                                    #
#         CRECK Modeling Group <http://creckmodeling.chem.polimi.it>                 #
#         Department of Chemistry, Materials and Chemical Engineering                #
#         Politecnico di Milano, P.zza Leonardo da Vinci 32, 20133 Milano            #
#                                                                                    #
# ---------------------------------------------------------------------------------- #
import os
import warnings
import numpy as np
import xml.etree.ElementTree as ET

from .KineticMap import KineticMap


class OpenSMOKEppXMLFile:
    def __init__(self, output_folder: str, kinetic_folder: str) -> None:
        kinetic_map = KineticMap(kinetic_folder)
        xml_file_name = os.path.join(output_folder, "Output.xml")
        tree = ET.parse(xml_file_name)
        root = tree.getroot()

        # System types
        new_system_types = ["HomogeneousReactor", "Flamelet", "Flame1D", "Flame2D"]
        old_system_types = ["BatchReactor", "PlugFlowReactor", "PerfectlyStirredReactor"]
        system_type = ((root.find("Type")).text).strip()
        if system_type not in new_system_types:
            if system_type in old_system_types:
                warnings.warn(
                    " * WARNING: You are running an older version of OpenSMOKE++ that is no longer mantained! Some of \
                    the functions in this class may not work!"
                )
            else:
                raise Exception(f"Unknown system type: {system_type}")

        # Check simulation/kinetics consistency
        dummy = root.find("mass-fractions")
        dummy = (dummy.text).split()
        list_names = []
        column_index_of_massfractions_profiles = []
        for i in range(int(dummy[0])):
            list_names.append(dummy[1 + i * 3])
            column_index_of_massfractions_profiles.append(int(dummy[3 + i * 3]))
        if len(list_names) != kinetic_map.number_of_species:
            raise Exception("The kinetic mechanism is not consistent with the simulation")

        # Recover additional variables
        dummy = root.find("additional")
        dummy = (dummy.text).split("\n")
        dummy = [i for i in dummy if not i.isnumeric() and i != ""]
        n_additional = len(dummy)
        additional_variable = [i.split()[0] + " " + i.split()[1] for i in dummy]
        index = [int(i.split()[-1]) for i in dummy]
        add_var_idx = index

        # List of possible variables
        self._time = None
        self._T = None
        self._P = None
        self._MW = None
        self._rho = None
        self._Q = None
        self._x_coord = None
        self._y_coord = None
        self._z_coord = None
        self._x_vel = None
        self._y_vel = None
        self._z_vel = None
        self._V = None
        self._csi = None
        self._tau = None
        self._chi_st = None
        self._strain_rate = None
        self._curvature = None
        self._enthalpy_sens = None
        self._cp = None
        self._therm_cond = None
        self._viscosity = None
        self._YSoot = None
        self._fvSOOT = None

        index_T = None
        index_P = None
        index_MW = None
        index_rho = None
        index_Q = None
        index_x_coord = None
        index_y_coord = None
        index_z_coord = None
        index_x_vel = None
        index_y_vel = None
        index_z_vel = None
        index_V = None
        index_csi = None
        index_tau = None
        index_chi_st = None
        index_strain_rate = None
        index_curvature = None
        index_enthalpy_sens = None
        index_cp = None
        index_therm_cond = None
        index_viscosity = None
        index_YSoot = None
        index_fvSOOT = None

        for i, j in enumerate(additional_variable):
            if "temperature" in j:
                index_T = index[i] - 2
            if "pressure" in j:
                index_P = index[i] - 2
            if "mol-weight" in j:
                index_MW = index[i] - 2
            if "density" in j:
                index_rho = index[i] - 2
            if "heat-release" in j:
                index_Q = index[i] - 2
            if "x-coord" in j:
                index_x_coord = index[i] - 2
            if "y-coord" in j:
                index_y_coord = index[i] - 2
            if "z-coord" in j:
                index_z_coord = index[i] - 2
            if "x-vel" in j:
                index_x_vel = index[i] - 2
            if "y-vel" in j:
                index_y_vel = index[i] - 2
            if "z-vel" in j:
                index_z_vel = index[i] - 2
            if "volume" in j:
                index_V = index[i] - 2
            if "tau" in j:
                index_tau = index[i] - 2
            if "chi-st" in j:
                index_chi_st = index[i] - 2
            if "strain-rate" in j:
                index_strain_rate = index[i] - 2
            if "curvature" in j:
                index_curvature = index[i] - 2
            if "enthalpy-sens" in j:
                index_enthalpy_sens = index[i] - 2
            if "cp" in j:
                index_cp = index[i] - 2
            if "therm-cond" in j:
                index_therm_cond = index[i] - 2
            if "viscosity" in j:
                index_viscosity = index[i] - 2
            if "YSoot" in j:
                index_YSoot = index[i] - 2
            if "csi" in j:
                index_csi = index[i] - 2
            if "mixture-fraction" in j or "mix-fract" in j:
                index_csi = index[i] - 2
            if "axial-coordinate" in j:
                index_csi = index[i] - 2
            if "fvSoot" in j:
                index_fvSOOT = index[i] - 2

        # Read profiles
        profiles_size = root.find("profiles-size")
        profiles_size = (profiles_size.text).split()
        npts = int(profiles_size[0])
        nc = n_additional + kinetic_map.number_of_species

        profiles = root.find("profiles")
        profiles = (profiles.text).split()
        profiles = np.reshape(profiles, (npts, nc))
        profiles = np.float32(profiles)

        # Extract relevant profiles

        self._time = profiles[:, 0]
        self._T = profiles[:, index_T]
        self._P = profiles[:, index_P]
        self._MW = profiles[:, index_MW]
        self._rho = profiles[:, index_rho]
        self._x_coord = profiles[:, index_x_coord]
        self._y_coord = profiles[:, index_y_coord]
        self._z_coord = profiles[:, index_z_coord]
        self._x_vel = profiles[:, index_x_vel]
        self._y_vel = profiles[:, index_y_vel]
        self._z_vel = profiles[:, index_z_vel]
        self._fvSOOT = profiles[:, index_fvSOOT]
        self._Q = profiles[:, index_Q]
        self._V = profiles[:, index_V]
        self._tau = profiles[:, index_tau]
        self._chi_st = profiles[:, index_chi_st]
        self._strain_rate = profiles[:, index_strain_rate]
        self._curvature = profiles[:, index_curvature]
        self._enthalpy_sens = profiles[:, index_enthalpy_sens]
        self._cp = profiles[:, index_cp]
        self._therm_cond = profiles[:, index_therm_cond]
        self._viscosity = profiles[:, index_viscosity]
        self._YSoot = profiles[:, index_YSoot]

        if system_type == "Flame1D":
            self._csi = profiles[:, index_csi]
        elif system_type == "Flamelet":
            self._csi = [1] * npts - profiles[:, index_csi]
        else:
            self._csi = [0] * npts

        # Composition
        Y = profiles[:, -kinetic_map.number_of_species:]
        X = Y * self._MW.reshape(-1, 1) / np.transpose(kinetic_map.mws.reshape(-1, 1))

        # Additional variables name
        for i in range(len(column_index_of_massfractions_profiles)):
            # Warning this can generate bugs
            if Y[0, column_index_of_massfractions_profiles[i] - len(additional_variable)] > 1e-8:
                additional_variable.append("conversion-" + list_names[i])

        # Assign internal members
        self._npts = npts
        self._ns = kinetic_map.number_of_species
        self._nc = nc

        self._Y = Y
        self._X = X

        self._additional_variable = additional_variable
        self._add_var_idx = add_var_idx
        self._kin = kinetic_map

    def mole_fraction(self, name: str):
        index_species = self._kin.index_from_species_name(name)
        return self._X[:, index_species]

    def mass_fraction(self, name: str):
        index_species = self._kin.index_from_species_name(name)
        return self._Y[:, index_species]

    @property
    def time(self):
        return self._time

    @property
    def T(self):
        return self._T

    @property
    def P(self):
        return self._P

    @property
    def MW(self):
        return self._MW

    @property
    def rho(self):
        return self._rho

    @property
    def Q(self):
        return self._Q

    @property
    def x_coord(self):
        return self._x_coord

    @property
    def y_coord(self):
        return self._y_coord

    @property
    def z_coord(self):
        return self._z_coord

    @property
    def x_vel(self):
        return self._x_vel

    @property
    def y_vel(self):
        return self._y_vel

    @property
    def z_vel(self):
        return self._z_vel

    @property
    def V(self):
        return self._V

    @property
    def csi(self):
        return self._csi

    @property
    def tau(self):
        return self._tau

    @property
    def chi_st(self):
        return self._chi_st

    @property
    def strain_rate(self):
        return self._strain_rate

    @property
    def curvature(self):
        return self._curvature

    @property
    def enthalpy_sens(self):
        return self._enthalpy_sens

    @property
    def cp(self):
        return self._cp

    @property
    def therm_cond(self):
        return self._therm_cond

    @property
    def viscosity(self):
        return self._viscosity

    @property
    def YSoot(self):
        return self._YSoot

    @property
    def fvSOOT(self):
        return self._fvSOOT


# ---------------------------------------------------------------------------------- #
#                                                                                    #
#         Python wrapper around the OpenSMOKEpp Graphical Post Processor.            #
#         Copyright (C) 2024                                                         #
#             Timoteo Dinelli     <timoteo.dinelli@polimi.it>                        #
#             Luna Pratali Maffei <luna.pratali@polimi.it>                           #
#             Edoardo Ramalli     <edoardo.ramalli@polimi.it>                        #
#             Andrea Nobili       <anobili@stanford.edu>                             #
#                                                                                    #
#         This program is free software: you can redistribute it and/or modify       #
#         it under the terms of the GNU General Public License as published by       #
#         the Free Software Foundation, either version 3 of the License, or          #
#         (at your option) any later version.                                        #
#                                                                                    #
#         This program is distributed in the hope that it will be useful,            #
#         but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#         MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              #
#         GNU General Public License for more details.                               #
#                                                                                    #
#         You should have received a copy of the GNU General Public License          #
#         along with this program.  If not, see <https://www.gnu.org/licenses/>.     #
#                                                                                    #
# ---------------------------------------------------------------------------------- #
