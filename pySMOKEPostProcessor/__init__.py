from .postprocessor_backend import postprocessor_backend_obj as _backend
from .simulation_utilities import GetSimulationsBoundary
from .ropa import RateOfProductionAnalysis

def load(lib_file_path: str):
	"""
	Attempt to load the SPLINTER back-end from the file at lib_file_path.
	lib_file_path should be the shared library file (.so on Linux, etc.)
	:param lib_file_path:
	:return:
	"""
	_backend.load(lib_file_path)

__all__ = [
	"simulation_utilities",
	"ropa"
]

try:
	_backend.load()
except Exception as e:
	print(e)

# Important to set this after the SPLINTER backend has been loaded
__version__ = _backend.version
