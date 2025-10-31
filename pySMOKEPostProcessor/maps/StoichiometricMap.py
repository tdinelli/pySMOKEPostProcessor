# ---------------------------------------------------------------------------------- #
#                                                                                    #
#                              _____  __  ___ ____   __ __  ______                   #
#                ____   __  __/ ___/ /  |/  // __ \ / //_/ / ____/____   ____        #
#               / __ \ / / / /\__ \ / /|_/ // / / // ,<   / __/  / __ \ / __ \       #
#              / /_/ // /_/ /___/ // /  / // /_/ // /| | / /___ / /_/ // /_/ /       #
#             / .___/ \__, //____//_/  /_/ \____//_/ |_|/_____// .___// .___/        #
#            /_/     /____/                                   /_/    /_/             #
#                                                                                    #
#                                                                                    #
# ---------------------------------------------------------------------------------- #
# Please refer to the copyright statement and license                                #
# information at the end of this file.                                               #
# ---------------------------------------------------------------------------------- #
#                                                                                    #
#         Authors: Timoteo Dinelli     <timoteo.dinelli@polimi.it>                   #
#                  Luna Pratali Maffei <luna.pratali@polimi.it>                      #
#                  Edoardo Ramalli     <edoardo.ramalli@polimi.it>                   #
#                  Andrea Nobili       <edoardo.ramalli@polimi.it>                   #
#                                                                                    #
#         CRECK Modeling Group <http://creckmodeling.chem.polimi.it>                 #
#         Department of Chemistry, Materials and Chemical Engineering                #
#         Politecnico di Milano, P.zza Leonardo da Vinci 32, 20133 Milano            #
#                                                                                    #
# ---------------------------------------------------------------------------------- #
import os
import sys
import numpy as np
from scipy import sparse
import xml.etree.ElementTree as ET

# Internal modules
from .KineticMap import KineticMap


class StoichiometricMap:

    def __init__(self, kinetic_folder):

        self.kinetics = KineticMap(kinetic_folder)
        kinetic_xml = os.path.join(kinetic_folder, "kinetics.xml")
        self.stoichiometry = read_stoichiometry(kinetic_xml)
        self.stoichiometry_processing(self.stoichiometry)
        self.nur = self.stoichiometry_coeff_reactants(self.kinetics)
        self.nup = self.stoichiometry_coeff_products(self.kinetics)

    @staticmethod
    def read_vector_int(vector, pos):
        length = int(vector[pos])
        subvector = vector[pos + 1 : pos + length + 1]
        return np.int32(subvector), pos + length + 1

    @staticmethod
    def read_vector_float64(vector, pos):
        length = int(vector[pos])
        subvector = vector[pos + 1 : pos + length + 1]
        return np.float64(subvector), pos + length + 1

    @staticmethod
    def read_stoichiometry(kinetics_xml):
        tree = ET.parse(kinetics_xml)
        root = tree.getroot()
        kinetics_element = root.find("Kinetics")
        stoichiometry_element = kinetics_element.find("Stoichiometry")
        stoichiometry = (stoichiometry_element.text).split()
        return stoichiometry

    def stoichiometry_processing(self, stoichiometry):

        pos = 0
        numDir1, pos = read_vector_int(stoichiometry, pos)
        numDir2, pos = read_vector_int(stoichiometry, pos)
        numDir3, pos = read_vector_int(stoichiometry, pos)
        numDir4, pos = read_vector_int(stoichiometry, pos)
        numDir5, pos = read_vector_int(stoichiometry, pos)

        numRevTot1, pos = read_vector_int(stoichiometry, pos)
        numRevTot2, pos = read_vector_int(stoichiometry, pos)
        numRevTot3, pos = read_vector_int(stoichiometry, pos)
        numRevTot4, pos = read_vector_int(stoichiometry, pos)
        numRevTot5, pos = read_vector_int(stoichiometry, pos)

        numRevEq1, pos = read_vector_int(stoichiometry, pos)
        numRevEq2, pos = read_vector_int(stoichiometry, pos)
        numRevEq3, pos = read_vector_int(stoichiometry, pos)
        numRevEq4, pos = read_vector_int(stoichiometry, pos)
        numRevEq5, pos = read_vector_int(stoichiometry, pos)

        jDir1, pos = read_vector_int(stoichiometry, pos)
        jDir2, pos = read_vector_int(stoichiometry, pos)
        jDir3, pos = read_vector_int(stoichiometry, pos)
        jDir4, pos = read_vector_int(stoichiometry, pos)
        jDir5, pos = read_vector_int(stoichiometry, pos)
        valueDir5, pos = read_vector_float64(stoichiometry, pos)

        jDir1 = jDir1 - 1
        jDir2 = jDir2 - 1
        jDir3 = jDir3 - 1
        jDir4 = jDir4 - 1
        jDir5 = jDir5 - 1

        jRevTot1, pos = read_vector_int(stoichiometry, pos)
        jRevTot2, pos = read_vector_int(stoichiometry, pos)
        jRevTot3, pos = read_vector_int(stoichiometry, pos)
        jRevTot4, pos = read_vector_int(stoichiometry, pos)
        jRevTot5, pos = read_vector_int(stoichiometry, pos)
        valueRevTot5, pos = read_vector_float64(stoichiometry, pos)

        jRevTot1 = jRevTot1 - 1
        jRevTot2 = jRevTot2 - 1
        jRevTot3 = jRevTot3 - 1
        jRevTot4 = jRevTot4 - 1
        jRevTot5 = jRevTot5 - 1

        jRevEq1, pos = read_vector_int(stoichiometry, pos)
        jRevEq2, pos = read_vector_int(stoichiometry, pos)
        jRevEq3, pos = read_vector_int(stoichiometry, pos)
        jRevEq4, pos = read_vector_int(stoichiometry, pos)
        jRevEq5, pos = read_vector_int(stoichiometry, pos)
        valueRevEq5, pos = read_vector_float64(stoichiometry, pos)

        jRevEq1 = jRevEq1 - 1
        jRevEq2 = jRevEq2 - 1
        jRevEq3 = jRevEq3 - 1
        jRevEq4 = jRevEq4 - 1
        jRevEq5 = jRevEq5 - 1

        changeOfMoles, pos = read_vector_float64(stoichiometry, pos)
        explicit_reaction_orders = int(stoichiometry[pos])

        # Elementary reactions only
        if explicit_reaction_orders == 0:

            lambda_numDir1 = numDir1
            lambda_numDir2 = numDir2
            lambda_numDir3 = numDir3
            lambda_numDir4 = numDir4
            lambda_numDir5 = numDir5

            lambda_numRevEq1 = numRevEq1
            lambda_numRevEq2 = numRevEq2
            lambda_numRevEq3 = numRevEq3
            lambda_numRevEq4 = numRevEq4
            lambda_numRevEq5 = numRevEq5

            lambda_jDir1 = jDir1
            lambda_jDir2 = jDir2
            lambda_jDir3 = jDir3
            lambda_jDir4 = jDir4
            lambda_jDir5 = jDir5
            lambda_valueDir5 = valueDir5

            lambda_jRevEq1 = jRevEq1
            lambda_jRevEq2 = jRevEq2
            lambda_jRevEq3 = jRevEq3
            lambda_jRevEq4 = jRevEq4
            lambda_jRevEq5 = jRevEq5
            lambda_valueRevEq5 = valueRevEq5

        else:
            sys.exit("Non-elementary reactions cannot be processed")

        self.numDir1 = numDir1
        self.numDir2 = numDir2
        self.numDir3 = numDir3
        self.numDir4 = numDir4
        self.numDir5 = numDir5

        self.numRevTot1 = numRevTot1
        self.numRevTot2 = numRevTot2
        self.numRevTot3 = numRevTot3
        self.numRevTot4 = numRevTot4
        self.numRevTot5 = numRevTot5

        self.numRevEq1 = numRevEq1
        self.numRevEq2 = numRevEq2
        self.numRevEq3 = numRevEq3
        self.numRevEq4 = numRevEq4
        self.numRevEq5 = numRevEq5

        self.jDir1 = jDir1
        self.jDir2 = jDir2
        self.jDir3 = jDir3
        self.jDir4 = jDir4
        self.jDir5 = jDir5

        self.jRevTot1 = jRevTot1
        self.jRevTot2 = jRevTot2
        self.jRevTot3 = jRevTot3
        self.jRevTot4 = jRevTot4
        self.jRevTot5 = jRevTot5
        self.valueRevTot5 = valueRevTot5

        self.jRevEq1 = jRevEq1
        self.jRevEq2 = jRevEq2
        self.jRevEq3 = jRevEq3
        self.jRevEq4 = jRevEq4
        self.jRevEq5 = jRevEq5
        self.valueRevEq5 = valueRevEq5

        self.lambda_numDir1 = lambda_numDir1
        self.lambda_numDir2 = lambda_numDir2
        self.lambda_numDir3 = lambda_numDir3
        self.lambda_numDir4 = lambda_numDir4
        self.lambda_numDir5 = lambda_numDir5

        self.lambda_numRevEq1 = lambda_numRevEq1
        self.lambda_numRevEq2 = lambda_numRevEq2
        self.lambda_numRevEq3 = lambda_numRevEq3
        self.lambda_numRevEq4 = lambda_numRevEq4
        self.lambda_numRevEq5 = lambda_numRevEq5

        self.lambda_jDir1 = lambda_jDir1
        self.lambda_jDir2 = lambda_jDir2
        self.lambda_jDir3 = lambda_jDir3
        self.lambda_jDir4 = lambda_jDir4
        self.lambda_jDir5 = lambda_jDir5
        self.lambda_valueDir5 = lambda_valueDir5

        self.lambda_jRevEq1 = lambda_jRevEq1
        self.lambda_jRevEq2 = lambda_jRevEq2
        self.lambda_jRevEq3 = lambda_jRevEq3
        self.lambda_jRevEq4 = lambda_jRevEq4
        self.lambda_jRevEq5 = lambda_jRevEq5
        self.lambda_valueRevEq5 = lambda_valueRevEq5

    def stoichiometry_coeff_reactants(self, kinetics):
        react_species = []
        react_reaction = []
        react_nu = []

        count1 = 0
        count2 = 0
        count3 = 0
        count4 = 0
        count5 = 0
        for i in range(kinetics.number_of_species):
            for _ in range(self.numDir1[i]):
                react_species.append(i)
                react_reaction.append(self.jDir1[count1])
                react_nu.append(1.0)
                count1 = count1 + 1

            for _ in range(self.numDir2[i]):
                react_species.append(i)
                react_reaction.append(self.jDir2[count2])
                react_nu.append(2.0)
                count2 = count2 + 1

            for _ in range(self.numDir3[i]):
                react_species.append(i)
                react_reaction.append(self.jDir3[count3])
                react_nu.append(3.0)
                count3 = count3 + 1

            for _ in range(self.numDir4[i]):
                react_species.append(i)
                react_reaction.append(self.jDir4[count4])
                react_nu.append(0.5)
                count4 = count4 + 1

            for _ in range(self.numDir5[i]):
                react_species.append(i)
                react_reaction.append(self.jDir5[count5])
                react_nu.append(self.valueDir5[count5])
                count5 = count5 + 1

        self.nur = sparse.coo_matrix(
            (react_nu, (react_reaction, react_species)), shape=(kinetics.NumberOfReactions, kinetics.number_of_species)
        )

        return self.nur

    def stoichiometry_coeff_products(self, kinetics):
        react_species = []
        react_reaction = []
        react_nu = []

        count1 = 0
        count2 = 0
        count3 = 0
        count4 = 0
        count5 = 0
        for i in range(kinetics.number_of_species):

            for _ in range(self.numRevTot1[i]):
                react_species.append(i)
                react_reaction.append(self.jRevTot1[count1])
                react_nu.append(1.0)
                count1 = count1 + 1

            for _ in range(self.numRevTot2[i]):
                react_species.append(i)
                react_reaction.append(self.jRevTot2[count2])
                react_nu.append(2.0)
                count2 = count2 + 1

            for _ in range(self.numRevTot3[i]):
                react_species.append(i)
                react_reaction.append(self.jRevTot3[count3])
                react_nu.append(3.0)
                count3 = count3 + 1

            for _ in range(self.numRevTot4[i]):
                react_species.append(i)
                react_reaction.append(self.jRevTot4[count4])
                react_nu.append(0.5)
                count4 = count4 + 1

            for _ in range(self.numRevTot5[i]):
                react_species.append(i)
                react_reaction.append(self.jRevTot5[count5])
                react_nu.append(self.valueRevTot5[count5])
                count5 = count5 + 1

        self.nup = sparse.coo_matrix(
            (react_nu, (react_reaction, react_species)), shape=(kinetics.NumberOfReactions, kinetics.number_of_species)
        )

        return self.nup

    def reaction_order_reactants(self, kinetics):
        react_species = []
        react_reaction = []
        react_lambda = []

        count1 = 0
        count2 = 0
        count3 = 0
        count4 = 0
        count5 = 0
        for i in range(kinetics.number_of_species):
            for _ in range(self.lambda_numDir1[i]):
                react_species.append(i)
                react_reaction.append(self.lambda_jDir1[count1])
                react_lambda.append(1.0)
                count1 = count1 + 1

            for _ in range(self.lambda_numDir2[i]):
                react_species.append(i)
                react_reaction.append(self.lambda_jDir2[count2])
                react_lambda.append(2.0)
                count2 = count2 + 1

            for _ in range(self.lambda_numDir3[i]):
                react_species.append(i)
                react_reaction.append(self.lambda_jDir3[count3])
                react_lambda.append(3.0)
                count3 = count3 + 1

            for _ in range(self.lambda_numDir4[i]):
                react_species.append(i)
                react_reaction.append(self.lambda_jDir4[count4])
                react_lambda.append(0.5)
                count4 = count4 + 1

            for _ in range(self.lambda_numDir5[i]):
                react_species.append(i)
                react_reaction.append(self.lambda_jDir5[count5])
                react_lambda.append(self.lambda_valueDir5[count5])
                count5 = count5 + 1

        self.lambdar = sparse.coo_matrix(
            (react_lambda, (react_reaction, react_species)),
            shape=(kinetics.NumberOfReactions, kinetics.number_of_species),
        )

        return self.lambdar

    def reaction_order_products(self, kinetics):
        react_species = []
        react_reaction = []
        react_lambda = []

        count1 = 0
        count2 = 0
        count3 = 0
        count4 = 0
        count5 = 0
        for i in range(kinetics.number_of_species):
            for _ in range(self.lambda_numRevEq1[i]):
                react_species.append(i)
                react_reaction.append(self.lambda_jRevEq1[count1])
                react_lambda.append(1.0)
                count1 = count1 + 1

            for _ in range(self.lambda_numRevEq2[i]):
                react_species.append(i)
                react_reaction.append(self.lambda_jRevEq2[count2])
                react_lambda.append(2.0)
                count2 = count2 + 1

            for _ in range(self.lambda_numRevEq3[i]):
                react_species.append(i)
                react_reaction.append(self.lambda_jRevEq3[count3])
                react_lambda.append(3.0)
                count3 = count3 + 1

            for _ in range(self.lambda_numRevEq4[i]):
                react_species.append(i)
                react_reaction.append(self.lambda_jRevEq4[count4])
                react_lambda.append(0.5)
                count4 = count4 + 1

            for _ in range(self.lambda_numRevEq5[i]):
                react_species.append(i)
                react_reaction.append(self.lambda_jRevEq5[count5])
                react_lambda.append(self.lambda_valueRevEq5[count5])
                count5 = count5 + 1

        self.lambdap = sparse.coo_matrix(
            (react_lambda, (react_reaction, react_species)),
            shape=(kinetics.NumberOfReactions, kinetics.number_of_species),
        )

        return self.lambdap


# ---------------------------------------------------------------------------------- #
#                                                                                    #
#         Python wrapper around the OpenSMOKEpp Graphical Post Processor.            #
#         Copyright (C) 2024                                                         #
#             Timoteo Dinelli     <timoteo.dinelli@polimi.it>                        #
#             Luna Pratali Maffei <luna.pratali@polimi.it>                           #
#             Edoardo Ramalli     <edoardo.ramalli@polimi.it>                        #
#             Andrea Nobili       <anobili@stanford.edu>                             #
#                                                                                    #
#         This program is free software: you can redistribute it and/or modify       #
#         it under the terms of the GNU General Public License as published by       #
#         the Free Software Foundation, either version 3 of the License, or          #
#         (at your option) any later version.                                        #
#                                                                                    #
#         This program is distributed in the hope that it will be useful,            #
#         but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#         MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              #
#         GNU General Public License for more details.                               #
#                                                                                    #
#         You should have received a copy of the GNU General Public License          #
#         along with this program.  If not, see <https://www.gnu.org/licenses/>.     #
#                                                                                    #
# ---------------------------------------------------------------------------------- #
