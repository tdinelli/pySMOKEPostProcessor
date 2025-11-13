#include "PostProcessorWrapper_py.h"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "source/ProfilesDatabase.h"
#include "source/ROPA.h"
#include "source/Sensitivities.h"

namespace py = pybind11;
constexpr auto byref = py::return_value_policy::reference_internal;

PYBIND11_MODULE(pySMOKEPostProcessor, m) {
  m.doc() = "Python Interface to the OpenSMOKEpp Graphical Post Processor";

  py::class_<ProfilesDatabase>(m, "ProfilesDatabase")
      .def(py::init<>())
      .def("readKineticMechanism", &ProfilesDatabase::ReadKineticMechanism,
           py::call_guard<py::gil_scoped_release>())
      .def("readFileResults", &ProfilesDatabase::ReadFileResults,
           py::call_guard<py::gil_scoped_release>())
      .def("prepare", &ProfilesDatabase::Prepare, py::call_guard<py::gil_scoped_release>())
      .def("prepare", &ProfilesDatabase::Prepare, py::call_guard<py::gil_scoped_release>());

  py::class_<ROPA>(m, "ROPA")
      .def(py::init<>())
      .def("setDataBase", &ROPA::SetDatabase, py::call_guard<py::gil_scoped_release>())
      .def("rateOfProductionAnalysis", &ROPA::RateOfProductionAnalysis,
           py::call_guard<py::gil_scoped_release>())
      .def("ropa", &ROPA::RateOfProductionAnalysis2D, py::call_guard<py::gil_scoped_release>())
      .def("fluxAnalysis", &ROPA::FluxAnalysis, py::call_guard<py::gil_scoped_release>())
      .def("getReactionRates", &ROPA::GetReactionRates, py::call_guard<py::gil_scoped_release>())
      .def("getFormationRates", &ROPA::GetFormationRates, py::call_guard<py::gil_scoped_release>())
      .def("setKineticFolder", &ROPA::SetKineticFolder, py::call_guard<py::gil_scoped_release>())
      .def("setOutputFolder", &ROPA::SetOutputFolder, py::call_guard<py::gil_scoped_release>())
      .def("setROPAType", &ROPA::SetROPAType, py::call_guard<py::gil_scoped_release>())
      .def("setSpecies", &ROPA::SetSpecies, py::call_guard<py::gil_scoped_release>())
      .def("setLocalValue", &ROPA::SetLocalValue, py::call_guard<py::gil_scoped_release>())
      .def("setLowerBound", &ROPA::SetLowerBound, py::call_guard<py::gil_scoped_release>())
      .def("setUpperBound", &ROPA::SetUpperBound, py::call_guard<py::gil_scoped_release>())
      .def("setElement", &ROPA::SetElement, py::call_guard<py::gil_scoped_release>())
      .def("setThickness", &ROPA::SetThickness, py::call_guard<py::gil_scoped_release>())
      .def("setFluxAnalysisType", &ROPA::SetFluxAnalysisType,
           py::call_guard<py::gil_scoped_release>())
      .def("setWidth", &ROPA::SetWidth, py::call_guard<py::gil_scoped_release>())
      .def("setDepth", &ROPA::SetDepth, py::call_guard<py::gil_scoped_release>())
      .def("setThreshold", &ROPA::SetThreshold, py::call_guard<py::gil_scoped_release>())
      .def("setThicknessLogScale", &ROPA::SetThicknessLogScale,
           py::call_guard<py::gil_scoped_release>())
      .def("setLabelType", &ROPA::SetLabelType, py::call_guard<py::gil_scoped_release>())
      .def("reactions", &ROPA::reactions, py::call_guard<py::gil_scoped_release>())
      .def("coefficients", &ROPA::coefficients, py::call_guard<py::gil_scoped_release>())
      .def("indexFirstName", &ROPA::indexFirstName, py::call_guard<py::gil_scoped_release>())
      .def("indexSecondName", &ROPA::indexSecondName, py::call_guard<py::gil_scoped_release>())
      .def("computedThickness", &ROPA::computedThickness, py::call_guard<py::gil_scoped_release>())
      .def("computedLabel", &ROPA::computedLabel, py::call_guard<py::gil_scoped_release>())
      .def("formationRates", &ROPA::formationRates, py::call_guard<py::gil_scoped_release>())
      .def("reactionRates", &ROPA::reactionRates, py::call_guard<py::gil_scoped_release>())
      .def("sumOfRates", &ROPA::sumOfRates, py::call_guard<py::gil_scoped_release>());

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
      .def("sensitivityCoefficients", &Sensitivities::senitivityCoefficients,
           py::call_guard<py::gil_scoped_release>());
}
