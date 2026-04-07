from pySMOKEPostProcessor import PostProcessor, script_utils
import xml.etree.ElementTree as ET # It is required for what I have in mind. Maybe we move this to CXX_Wrapper and save the variable from there.
import os   # Required for ET, if removed take this out as well
import numpy as np
import pandas as pd
from scipy.integrate import cumulative_trapezoid

class CumulativeDeposition:
    """
    Parameters
    ----------
    kineticFolder : string
                Pointer to the folder containing the kinetics.surface.xml and surface_reaction_names.xml files
    outputFolder:   string
                Pointer to the folder containing the Output.xml file

    allCarbon:      bool
                Decide if deposition is evaluated on all bulk species or on C(B) only.
                TODO: at the moment, only the False option is available

    """
    def __init__(self,
                kineticFolder: str,
                outputFolder: str,
                class_group_file: str,
                allCarbon: bool = False,
                sort_type = [['reactiontype']]):

        self.kineticFolder = kineticFolder
        self.outputFolder = outputFolder
        
        targets = ['C(B)']
        if allCarbon:
            print("Error! allCarbon option not implemented yet.")
            return None
            targets.append('c(B)')  # Non mi piace nemmeno hardcoded, va fatto meglio
        self.targets = targets
        self.sort_type = sort_type    # Default classification option
        rxns_sorted = script_utils.get_sortedrxns(kineticFolder, class_group_file, heterogeneous_reactions=True)
        self.rxns_sorted = rxns_sorted

    def setClassification(self, sort_type):
        self.sort_type = sort_type
    
    def plotCumulativeDeposition(self,
                    profilesTag: str = 'profiles',
                    lump_steps: int = 1):
        # The tag argument is only useful for phases where it has a different name (Riccardo...)
        timesteps = self.getTimeProfile(tag=profilesTag)

        df_ROPAt = []
        for i in range(int(len(timesteps)/lump_steps)): # è stra lento nel chiamare Ny volte la funzione perché re-inizializza tutto ad ogni iter;
                            # o si riscrive da capo o si trova un workaround
            i_lump = i*lump_steps
            df = script_utils.process_classes(
                    simul_fld=self.outputFolder,kin_xml_fld=self.kineticFolder, rxns_sorted_obj=self.rxns_sorted,
                    species_list=self.targets,  sortlists=self.sort_type,       heterogeneous_reactions=True,
                    ropa_type='local',          local_value=timesteps[i_lump],       weigh='false')
            if isinstance(df, list):
                for d in df:
                    d["time"] = timesteps[i_lump]
                df_ROPAt.extend(df)
            else:
                df["time"] = timesteps[i_lump]
                df_ROPAt.append(df)
        df_ROPAt = pd.concat(df_ROPAt, ignore_index=True)
        df_ROPAt = df_ROPAt.fillna(0)
        self.ROPAbyClass_t = df_ROPAt
        df_ROPAintegral = self.getROPAIntegralTimeHistory(df_ROPAt)
        print(df_ROPAintegral)

    def getTimeProfile(self,tag='profiles'):
        
        output_root = ET.parse(os.path.join(self.outputFolder, "Output.xml")).getroot()
        node = output_root.find(tag)
        
        if node is None or node.text is None:
            raise ValueError(f"Tag '{tag}' not found or empty in the XML.")
        
        timesteps = np.fromiter( (float(line.split()[0]) for line in node.text.strip().splitlines() if line.strip()), dtype=float )
        return timesteps

    def getROPAIntegralTimeHistory(self, df_ROPAt):

        if "time" not in df_ROPAt.columns:
            raise ValueError("Column 'time' not found")

        time = df_ROPAt["time"].unique()
        Nt = len(time)

        cols = df_ROPAt.select_dtypes(include=[np.number]).columns.tolist()
        cols.remove("time")

        n_rows = len(df_ROPAt) // Nt
        data = df_ROPAt[cols].to_numpy().reshape(Nt, n_rows, len(cols))

        integ = cumulative_trapezoid(y=data, x=time, axis=0, initial=0)

        df_integrated = df_ROPAt.copy()
        df_integrated[cols] = integ.reshape(len(df_ROPAt), len(cols))

        return df_integrated