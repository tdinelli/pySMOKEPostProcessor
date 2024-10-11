#include "PostProcessorWrapper_py.h"

namespace py = pybind11;
constexpr auto byref = py::return_value_policy::reference_internal;
constexpr auto call_guard = py::call_guard<py::gil_scoped_release>();

#include "source/ProfilesDatabase.h"
#include "source/ROPA.h"
// #include "source/Sensitivities.h"


PYBIND11_MODULE(pySMOKEPostProcessor, m) {
  m.doc() = "Python Interface to the OpenSMOKEpp Graphical Post Processor";

  ProfilesDatabase::py_wrap(m);

  ROPA::py_wrap(m);

  // py::class_<Sensitivities>(m, "Sensitivity")
  //     .def(py::init<>())
  //     .def("setDataBase", &Sensitivities::SetDatabase,
  //          py::call_guard<py::gil_scoped_release>())
  //     .def("setNormalizationType", &Sensitivities::SetNormalizationType,
  //          py::call_guard<py::gil_scoped_release>())
  //     .def("setSensitivityType", &Sensitivities::SetSensitivityType,
  //          py::call_guard<py::gil_scoped_release>())
  //     .def("setOrderingType", &Sensitivities::SetOrderingType,
  //          py::call_guard<py::gil_scoped_release>())
  //     .def("setTarget", &Sensitivities::SetTarget,
  //          py::call_guard<py::gil_scoped_release>())
  //     .def("setLocalValue", &Sensitivities::SetLocalValue,
  //          py::call_guard<py::gil_scoped_release>())
  //     .def("setLowerBound", &Sensitivities::SetLowerBound,
  //          py::call_guard<py::gil_scoped_release>())
  //     .def("setUpperBound", &Sensitivities::SetUpperBound,
  //          py::call_guard<py::gil_scoped_release>())
  //     .def("prepare", &Sensitivities::Prepare, py::call_guard<py::gil_scoped_release>())
  //     .def("sensitivityAnalysis", &Sensitivities::Sensitivity_Analysis,
  //          py::call_guard<py::gil_scoped_release>())
  //     .def("readSensitivityCoefficients", &Sensitivities::ReadSensitvityCoefficients,
  //          py::call_guard<py::gil_scoped_release>())
  //     .def("getSensitivityProfile", &Sensitivities::GetSensitivityProfile,
  //          py::call_guard<py::gil_scoped_release>())
  //     .def("reactions", &Sensitivities::reactions,
  //          py::call_guard<py::gil_scoped_release>())
  //     .def("sensitivityCoefficients", &Sensitivities::senitivityCoefficients,
  //          py::call_guard<py::gil_scoped_release>());
}
