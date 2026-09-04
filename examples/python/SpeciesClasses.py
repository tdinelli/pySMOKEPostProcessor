import os

import matplotlib.pyplot as plt
from IPython.display import display

from pySMOKEPostProcessor import PostProcessor, plot_class_distribution, plot_heatmap

kineticFolder = os.path.join("..", "data", "SpeciesClasses", "kinetics")
resultsFolder = os.path.join("..", "data", "SpeciesClasses", "Output")

pp = PostProcessor(kineticFolder, resultsFolder)

# ---------------------------------------------------------------------------
# 1) Class-wise elemental distribution: how carbon moves C1 -> C2 -> PAH -> soot
#    along the batch-reactor time axis. Rows sum to 1, so the plot fills to 100%.
# ---------------------------------------------------------------------------
carbon = pp.ElementalDistributionByClass(element="C", normalize=True)
print(carbon.iloc[[0, len(carbon) // 2, -1]])

fig_c, ax_c = plot_class_distribution(
    carbon, xlabel="time [s]", ylabel="carbon fraction", title="Carbon distribution by class"
)

# ---------------------------------------------------------------------------
# 2) Flux-by-class at t = 0.5 s. The full directed class x class carbon-flux
#    matrix is always returned; the graph is a breadth-first walk from a seed.
#
#    flux_per_class=True (default) -> seed by class name.
#    carbon_weighted=True (default) -> OpenSMOKE's carbon-atom throughput; for a
#    soot mechanism the soot-soot block dominates. Pass carbon_weighted=False for
#    a per-reaction rate view that keeps lumped BIN classes comparable to the gas.
# ---------------------------------------------------------------------------
res = pp.FluxAnalysisByClass(
    element="C",
    flux_analysis_type="destruction",
    class_name="C2",
    flux_per_class=True,
    depth=3,
    width=5,
    threshold=1.0,
    local_value=0.5,
    carbon_weighted=True,
)

print(res["matrix"])
fig_m = plot_heatmap(res["matrix"], symmetricaxis=False, dftype="generic")
display(res["graph"])

# Same analysis, seeded from a species instead of a class, and using the
# bounded per-reaction weighting so the gas network stays visible.
res_sp = pp.FluxAnalysisByClass(
    element="C",
    flux_analysis_type="destruction",
    species_name="C2H2",
    flux_per_class=False,
    depth=3,
    width=5,
    threshold=1.0,
    local_value=0.5,
    carbon_weighted=False,
)
display(res_sp["graph"])

plt.show()
