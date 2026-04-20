#include "PostProcessorWrapper_py.h"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "source/ProfilesDatabase.h"
#include "source/ROPA.h"
#include "source/Sensitivities.h"
#include "source/ROPA_Surface.h"
#include "source/Sensitivities_Surface.h"

namespace py = pybind11;
constexpr auto byref = py::return_value_policy::reference_internal;

PYBIND11_MODULE(pySMOKEPostProcessor, m) {
  m.doc() = "Python Interface to the OpenSMOKEpp Graphical Post Processor";

  py::class_<ProfilesDatabase>(m, "ProfilesDatabase")
     .def(py::init<>())
     .def("readKineticMechanism",                 &ProfilesDatabase::ReadKineticMechanism,               py::arg("folder_name") = "kinetics",
                                                                                                         py::call_guard<py::gil_scoped_release>())
     .def("readHeterogeneousKineticMechanism",    &ProfilesDatabase::ReadHeterogeneousKineticMechanism,  py::arg("folder_name") = "kinetics",
                                                                                                         py::arg("phase_name")  = "Surface",
                                                                                                         py::call_guard<py::gil_scoped_release>())
     .def("readFileResults",                      &ProfilesDatabase::ReadFileResults,                    py::arg("folder_name") = "Output",
                                                                                                         py::arg("isHeterogeneous") = false,     // I think this parameter can be taken out entirely
                                                                                                         py::call_guard<py::gil_scoped_release>())
     .def("prepare",                              &ProfilesDatabase::Prepare,                            py::call_guard<py::gil_scoped_release>())
     .def("prepareHeterogeneous",                 &ProfilesDatabase::PrepareHeterogeneous,               py::call_guard<py::gil_scoped_release>());

  py::class_<ROPA>(m, "ROPA")
     .def(py::init<>())
     .def("setDataBase",                &ROPA::SetDatabase,                py::arg("data"),
                                                                           py::call_guard<py::gil_scoped_release>())
     .def("rateOfProductionAnalysis",   &ROPA::RateOfProductionAnalysis,   py::arg("number_of_reactions") = 10,
                                                                           py::call_guard<py::gil_scoped_release>())
     .def("ropa",                       &ROPA::RateOfProductionAnalysis2D, py::call_guard<py::gil_scoped_release>())    // TODO keyword arguments
     .def("fluxAnalysis",               &ROPA::FluxAnalysis,               py::call_guard<py::gil_scoped_release>())    // No arguments
     .def("getReactionRates",           &ROPA::GetReactionRates,           py::arg("reaction_indices"),
                                                                           py::arg("sum_rates") = false,
                                                                           py::call_guard<py::gil_scoped_release>())
     .def("getFormationRates",          &ROPA::GetFormationRates,          py::arg("specie"),
                                                                           py::arg("units"),
                                                                           py::arg("type"),
                                                                           py::call_guard<py::gil_scoped_release>())
     .def("setKineticFolder",           &ROPA::SetKineticFolder,           py::arg("kineticFolder") = "kinetics",
                                                                           py::call_guard<py::gil_scoped_release>())
     .def("setOutputFolder",            &ROPA::SetOutputFolder,            py::arg("outputFolder") = "Output",
                                                                           py::call_guard<py::gil_scoped_release>())
     .def("setROPAType",                &ROPA::SetROPAType,                py::arg("type") = "global",
                                                                           py::call_guard<py::gil_scoped_release>())
     .def("setSpecies",                 &ROPA::SetSpecies,                 py::arg("species"),
                                                                           py::call_guard<py::gil_scoped_release>())
     .def("setLocalValue",              &ROPA::SetLocalValue,              py::arg("localValue"),
                                                                           py::call_guard<py::gil_scoped_release>())
     .def("setLowerBound",              &ROPA::SetLowerBound,              py::arg("lowerBound"),
                                                                           py::call_guard<py::gil_scoped_release>())
     .def("setUpperBound",              &ROPA::SetUpperBound,              py::arg("upperBound"),
                                                                           py::call_guard<py::gil_scoped_release>())
     // TODO keyword args for flux analysis
     .def("setElement",                 &ROPA::SetElement,                 py::call_guard<py::gil_scoped_release>())
     .def("setThickness",               &ROPA::SetThickness,               py::call_guard<py::gil_scoped_release>())
     .def("setFluxAnalysisType",        &ROPA::SetFluxAnalysisType,        py::call_guard<py::gil_scoped_release>())
     .def("setWidth",                   &ROPA::SetWidth,                   py::call_guard<py::gil_scoped_release>())
     .def("setDepth",                   &ROPA::SetDepth,                   py::call_guard<py::gil_scoped_release>())
     .def("setThreshold",               &ROPA::SetThreshold,               py::call_guard<py::gil_scoped_release>())
     .def("setThicknessLogScale",       &ROPA::SetThicknessLogScale,       py::call_guard<py::gil_scoped_release>())
     .def("setLabelType",               &ROPA::SetLabelType,               py::call_guard<py::gil_scoped_release>())

     .def("reactions",                  &ROPA::reactions,                  py::call_guard<py::gil_scoped_release>())
     .def("coefficients",               &ROPA::coefficients,               py::call_guard<py::gil_scoped_release>())
     .def("indexFirstName",             &ROPA::indexFirstName,             py::call_guard<py::gil_scoped_release>())
     .def("indexSecondName",            &ROPA::indexSecondName,            py::call_guard<py::gil_scoped_release>())
     .def("computedThickness",          &ROPA::computedThickness,          py::call_guard<py::gil_scoped_release>())
     .def("computedLabel",              &ROPA::computedLabel,              py::call_guard<py::gil_scoped_release>())
     .def("formationRates",             &ROPA::formationRates,             py::call_guard<py::gil_scoped_release>())
     .def("reactionRates",              &ROPA::reactionRates,              py::call_guard<py::gil_scoped_release>())
     .def("sumOfRates",                 &ROPA::sumOfRates,                 py::call_guard<py::gil_scoped_release>());

 py::class_<ROPA_Surface, ROPA>(m, "ROPA_Surface")
     .def(py::init<>())
     .def("rateOfProductionAnalysis",   &ROPA_Surface::RateOfProductionAnalysis,     py::arg("number_of_reactions") = 10,
                                                                                     py::arg("heterogeneous_reactions") = true,
                                                                                     py::call_guard<py::gil_scoped_release>())
     .def("getReactionRates",           &ROPA_Surface::GetReactionRates,             py::arg("reaction_indices"),
                                                                                     py::arg("sum_rates") = false,
                                                                                     py::arg("heterogeneous_reactions") = false,
                                                                                     py::call_guard<py::gil_scoped_release>())
     .def("getFormationRates",           &ROPA_Surface::GetFormationRates,           py::arg("specie"),
                                                                                     py::arg("units") = "mole",
                                                                                     py::arg("type") = "net",
                                                                                     py::arg("heterogeneous_reactions") = false,
                                                                                     py::call_guard<py::gil_scoped_release>())
     .def("setROPAPhase",               &ROPA_Surface::SetROPAPhase,                 py::arg("heterogeneous_reactions") = true,
                                                                                     py::call_guard<py::gil_scoped_release>());

  py::class_<Sensitivities>(m, "Sensitivity")
     .def(py::init<>())
     .def("setDataBase", &Sensitivities::SetDatabase, py::call_guard<py::gil_scoped_release>())
     .def("setNormalizationType", &Sensitivities::SetNormalizationType,
          py::call_guard<py::gil_scoped_release>())
     .def("setSensitivityType", &Sensitivities::SetSensitivityType,
          py::call_guard<py::gil_scoped_release>())
     .def("setOrderingType", &Sensitivities::SetOrderingType,
          py::call_guard<py::gil_scoped_release>())
     .def("setTarget", &Sensitivities::SetTarget, py::call_guard<py::gil_scoped_release>())
     .def("setLocalValue", &Sensitivities::SetLocalValue, py::call_guard<py::gil_scoped_release>())
     .def("setLowerBound", &Sensitivities::SetLowerBound, py::call_guard<py::gil_scoped_release>())
     .def("setUpperBound", &Sensitivities::SetUpperBound, py::call_guard<py::gil_scoped_release>())
     .def("prepare", &Sensitivities::Prepare, py::call_guard<py::gil_scoped_release>())
     .def("sensitivityAnalysis", &Sensitivities::Sensitivity_Analysis,
          py::call_guard<py::gil_scoped_release>())
     .def("readSensitivityCoefficients", &Sensitivities::ReadSensitvityCoefficients,
          py::call_guard<py::gil_scoped_release>())
     .def("getSensitivityProfile", &Sensitivities::GetSensitivityProfile,
          py::call_guard<py::gil_scoped_release>())
     .def("reactions", &Sensitivities::reactions, py::call_guard<py::gil_scoped_release>())
     .def("sensitivityCoefficients", &Sensitivities::sensitivityCoefficients,
          py::call_guard<py::gil_scoped_release>());


  py::class_<Sensitivities_Surface>(m, "Sensitivity_Surface")
     .def(py::init<>())
     .def("setDataBase",                    &Sensitivities_Surface::SetDatabase,                   py::call_guard<py::gil_scoped_release>())
     .def("setNormalizationType",           &Sensitivities_Surface::SetNormalizationType,          py::call_guard<py::gil_scoped_release>())
     .def("setSensitivityType",             &Sensitivities_Surface::SetSensitivityType,            py::call_guard<py::gil_scoped_release>())
     .def("setOrderingType",                &Sensitivities_Surface::SetOrderingType,               py::call_guard<py::gil_scoped_release>())
     .def("setTarget",                      &Sensitivities_Surface::SetTarget,                     py::call_guard<py::gil_scoped_release>())
     .def("setLocalValue",                  &Sensitivities_Surface::SetLocalValue,                 py::call_guard<py::gil_scoped_release>())
     .def("setLowerBound",                  &Sensitivities_Surface::SetLowerBound,                 py::call_guard<py::gil_scoped_release>())
     .def("setUpperBound",                  &Sensitivities_Surface::SetUpperBound,                 py::call_guard<py::gil_scoped_release>())
     .def("prepare",                        &Sensitivities_Surface::Prepare,                       py::call_guard<py::gil_scoped_release>())
     .def("sensitivityAnalysis",            &Sensitivities_Surface::Sensitivity_Analysis,          py::call_guard<py::gil_scoped_release>())
     .def("readSensitivityCoefficients",    &Sensitivities_Surface::ReadSensitvityCoefficients,    py::call_guard<py::gil_scoped_release>())
     .def("getSensitivityProfile",          &Sensitivities_Surface::GetSensitivityProfile,         py::call_guard<py::gil_scoped_release>())
     .def("reactions",                      &Sensitivities_Surface::reactions,                     py::call_guard<py::gil_scoped_release>())
     .def("sensitivityCoefficients",        &Sensitivities_Surface::sensitivityCoefficients,       py::call_guard<py::gil_scoped_release>());
}
