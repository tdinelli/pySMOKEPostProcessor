// clang-format off
/*----------------------------------------------------------------------------------*\
|                                                                                    |
|                              _____  __  ___ ____   __ __  ______                   |
|                ____   __  __/ ___/ /  |/  // __ \ / //_/ / ____/____   ____        |
|               / __ \ / / / /\__ \ / /|_/ // / / // ,<   / __/  / __ \ / __ \       |
|              / /_/ // /_/ /___/ // /  / // /_/ // /| | / /___ / /_/ // /_/ /       |
|             / .___/ \__, //____//_/  /_/ \____//_/ |_|/_____// .___// .___/        |
|            /_/     /____/                                   /_/    /_/             |
|                                                                                    |
|                                                                                    |
| ---------------------------------------------------------------------------------- |
| Please refer to the copyright statement and license                                |
| information at the end of this file.                                               |
| ---------------------------------------------------------------------------------- |
|                                                                                    |
|         Authors: Timoteo Dinelli     <timoteo.dinelli@polimi.it>                   |
|                  Luna Pratali Maffei <luna.pratali@polimi.it>                      |
|                  Edoardo Ramalli     <edoardo.ramalli@polimi.it>                   |
|                  Andrea Nobili       <edoardo.ramalli@polimi.it>                   |
|                                                                                    |
|         CRECK Modeling Group <http://creckmodeling.chem.polimi.it>                 |
|         Department of Chemistry, Materials and Chemical Engineering                |
|         Politecnico di Milano, P.zza Leonardo da Vinci 32, 20133 Milano            |
|                                                                                    |
\*----------------------------------------------------------------------------------*/
// clang-format on

#include "PostProcessorWrapper_py.h"
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
// clang-format off
/*----------------------------------------------------------------------------------*\
|                                                                                    |
|         Python wrapper around the OpenSMOKEpp Graphical Post Processor.            |
|         Copyright (C) 2024                                                         |
|             Timoteo Dinelli     <timoteo.dinelli@polimi.it>                        |
|             Luna Pratali Maffei <luna.pratali@polimi.it>                           |
|             Edoardo Ramalli     <edoardo.ramalli@polimi.it>                        |
|             Andrea Nobili       <anobili@stanford.edu>                             |
|                                                                                    |
|         This program is free software: you can redistribute it and/or modify       |
|         it under the terms of the GNU General Public License as published by       |
|         the Free Software Foundation, either version 3 of the License, or          |
|         (at your option) any later version.                                        |
|                                                                                    |
|         This program is distributed in the hope that it will be useful,            |
|         but WITHOUT ANY WARRANTY; without even the implied warranty of             |
|         MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              |
|         GNU General Public License for more details.                               |
|                                                                                    |
|         You should have received a copy of the GNU General Public License          |
|         along with this program.  If not, see <https://www.gnu.org/licenses/>.     |
|                                                                                    |
\*----------------------------------------------------------------------------------*/
// clang-format on
