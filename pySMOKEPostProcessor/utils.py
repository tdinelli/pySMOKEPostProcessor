import os
from .postprocessor_backend import postprocessor_backend_obj as backend
from typing import List
from .utilities import *

def GetBoundary():
    
    kineticFolder = get_c_string('../examples/data/ROPA-01/kinetics')
    outputFolder = get_c_string('../examples/data/ROPA-01/Output')

    domain_maximum = list_to_c_array_of_doubles([0])
    domain_minimum = list_to_c_array_of_doubles([0])
    domain_middle = list_to_c_array_of_doubles([0])
    
    f_handle = backend.handle.getBoundary
    ciao = backend.call(f_handle, kineticFolder, outputFolder, domain_maximum, domain_minimum, domain_middle)
    
    domain_maximum = c_array_to_list(domain_maximum, 1)
    print(domain_maximum)