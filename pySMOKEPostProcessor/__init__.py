from .postprocessor_backend import postprocessor_backend_obj as _backend
from .simulation_utilities import GetSimulationsBoundary, GetSimulationINFO
from .ropa import RateOfProductionAnalysis, GetReactionRates, GetFormationRates, coeffs_to_df
from .sensitivity_analysis import SensitivityAnalysis, SensitivityCoefficients
from .flux_analysis import FluxAnalysis
from .reaction_classes import FluxByClass
from .plotting_utilities.heat_maps import plot_heatmap, save_fig
from .plotting_utilities.bar_plot import plot_bars

def load(lib_file_path: str):
	"""
	Attempt to load the pySMOKEPostProcessor back-end from the file at lib_file_path.
	lib_file_path should be the shared library file (.so on Linux, etc.)
	:param lib_file_path:
	:return:
	"""
	_backend.load(lib_file_path)

__all__ = [
	"simulation_utilities",
	"ropa",
	"sensitivity_analysis",
	"flux_analysis",
	"reaction_classes",
	"plotting_utilities.heat_maps",
	"plotting_utilities.bar_plot"
]

try:
	_backend.load()
except Exception as e:
	print(e)

# Important to set this after the pySMOKEPostProcessor backend has been loaded
__version__ = _backend.version
