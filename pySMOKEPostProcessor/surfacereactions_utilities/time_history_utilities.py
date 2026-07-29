import os
import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET
from scipy.integrate import cumulative_trapezoid

# The time profile should come from reading the Output.xml, maybe it is already saved somewhere and I don't remember it.
def getTimeProfile(outputFolder: str = "Output", 
                   tag: str ='profiles') -> np.array:
    """
    Returns a numpy array containing the time integration steps of the simulation.
    Args:
        outputFolder: string (default: "Output") with the path to the output FOLDER
        tag: string (default: "profiles") with the tag name for the profiles inside the XML file.
    Returns:
        timesteps: np.array
    """
    
    output_root = ET.parse(os.path.join(outputFolder, "Output.xml")).getroot()
    node = output_root.find(tag)
    
    if node is None or node.text is None:
        raise ValueError(f"Tag '{tag}' not found or empty in the XML.")
    
    timesteps = np.fromiter( (float(line.split()[0]) for line in node.text.strip().splitlines() if line.strip()), dtype=float )
    return timesteps

def getROPAIntegralTimeHistory(df_ROPAt: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a pandas.DataFrame object containing the integrated values of the ROPAs.
    Args: 
        df_ROPAt: pd.DataFrame containing local values of the ROPA
    Returns:
        df_integrated: pd.DataFrame containing integrated values of ROPA
    """

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