import os
from .postprocessor_backend import postprocessor_backend_obj as backend
from typing import List
from .utilities import *

def GetBoundary():
    from ctypes import c_double
    backend.load('/Users/tdinelli/Documents/GitHub/pySMOKEPostProcessor/build/libpySMOKEPostProcessor.dylib')
    path = os.path.join('..', 'build', 'libpySMOKEPostProcessor.dylib')
    kineticFolder = bytes('../examples/data/ROPA-02/kinetics', 'utf-8')
    outputFolder = bytes('../examples/data/ROPA-01/Output', 'utf-8')
    domain_maximum = (c_double*1)()
    domain_minimum = (c_double*1)()
    domain_middle = (c_double*1)()
    
    f_handle = backend.handle.getBoundary
    ciao = backend.call(f_handle, kineticFolder, outputFolder, domain_maximum, domain_minimum, domain_middle)
    
    domain_maximum = [i for i in domain_maximum][0]
    print(domain_maximum)