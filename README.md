# pySMOKEPostProcessor

Python wrapper around the OpenSMOKEpp Graphical post processor developed by Professor [Alberto Cuoci](http://creckmodeling.chem.polimi.it/menu-people/menu-people-faculty/menu-people-alberto-cuoci).
You can find the original repository of the OpenSMOKE Post Processor at this link (https://github.com/acuoci/OpenSMOKEppPostProcessor). Note that the original OpenSMOKEpp post processor was entirely
written in C++ and was based on the Qt5 libraries. Instead this version of the post processor exports and interfaces the computational C++ core of the original project dropping any dependencies on the
Qt5 libraries. Moreover extending most of the capabilities of the original post processor, see the examples for the details.

---

## Examples

The [examples](examples) folder contains a collection of [notebooks](examples/notebooks) and [python](examples/python) version of most of the capabilities of the package. Hereinafter are reported some of the main features.

### Features

- Rate Of Production Analysis. [notebook](examples/notebooks/RateOfProductionAnalysis.ipynb).
- Sensitivity Analysis. [notebook](examples/notebooks/SensitivityAnalysis.ipynb).
- Elementary Flux Analysis. [notebook](examples/notebooks/FluxAnalysis.ipynb).
- Reaction Rates plots. [notebook](examples/notebooks/Reaction_Rates.ipynb), [notebook-reactionclasses](examples/notebooks/Reaction_Rates_byclass.ipynb), [notebook-cumulative-reaction-rates](examples/notebooks/Cumulative-Rates.ipynb).
- Formation Rates plots. [notebook](examples/notebooks/FormationRates.ipynb).
- Sensitivity Coefficients plots. [notebook](examples/Sensitivity_Coefficients.ipynb).
- Rate Of Production Analysis by means of reaction classes. [notebook](examples/notebooks/Reaction_Classes.ipynb), [notebook-soot-FDI](examples/notebooks/Reaction_Classes_FDI.ipynb).

## Compile and Install

The detail explanation on how to build and install the package can be found inside the relative [documentation](doc/INSTALL.md).

# LICENSE

See the [LICENSE](LICENSE.md) file for license rights and limitations (GPL-3.0).

### DEVELOPERS notes
- https://sarcasm.github.io/notes/dev/compilation-database.html
- ninja -t compdb > compile_commands.json
- https://www.reddit.com/r/neovim/comments/18rbvzf/lsp_does_not_want_to_find_library_header_files/
