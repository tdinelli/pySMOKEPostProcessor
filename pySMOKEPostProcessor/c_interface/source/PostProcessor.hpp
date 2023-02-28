/*-----------------------------------------------------------------------*\
|    ___                   ____  __  __  ___  _  _______                  |
|   / _ \ _ __   ___ _ __ / ___||  \/  |/ _ \| |/ / ____| _     _         |
|  | | | | '_ \ / _ \ '_ \\___ \| |\/| | | | | ' /|  _| _| |_ _| |_       |
|  | |_| | |_) |  __/ | | |___) | |  | | |_| | . \| |__|_   _|_   _|      |
|   \___/| .__/ \___|_| |_|____/|_|  |_|\___/|_|\_\_____||_|   |_|        |
|        |_|                                                              |
|                                                                         |
|   Authors: Timoteo Dinelli <timoteo.dinelli@polimi.it>				  |
|			 Edoardo Ramalli <edoardo.ramalli@polimi.it>				  |
|   CRECK Modeling Group <http://creckmodeling.chem.polimi.it>            |
|   Department of Chemistry, Materials and Chemical Engineering           |
|   Politecnico di Milano                                                 |
|   P.zza Leonardo da Vinci 32, 20133 Milano                              |
|                                                                         |
|-------------------------------------------------------------------------|
|                                                                         |
|   This file is part of OpenSMOKE++ framework.                           |
|                                                                         |
|	License																  |
|                                                                         |
|   Copyright(C) 2016-2012  Alberto Cuoci                                 |
|   OpenSMOKE++ is free software: you can redistribute it and/or modify   |
|   it under the terms of the GNU General Public License as published by  |
|   the Free Software Foundation, either version 3 of the License, or     |
|   (at your option) any later version.                                   |
|                                                                         |
|   OpenSMOKE++ is distributed in the hope that it will be useful,        |
|   but WITHOUT ANY WARRANTY; without even the implied warranty of        |
|   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         |
|   GNU General Public License for more details.                          |
|                                                                         |
|   You should have received a copy of the GNU General Public License     |
|   along with OpenSMOKE++. If not, see <http://www.gnu.org/licenses/>.   |
|                                                                         |
\*-----------------------------------------------------------------------*/

#include "ROPA.h"
#include "Sensitivities.h"

PostProcessor::PostProcessor(std::string postporcessorType, std::string kineticFolder, std::string outputFolder)
{
	data_ = new ProfilesDatabase();
	postprocessorType_ = postporcessorType;
	kineticFolder_ = kineticFolder;
	outputFolder_ = outputFolder;
}

void PostProcessor::Prepare(std::string target, int type, double local_value, double lower_value, 
							double upper_value, int sensitivity_normalization_type, 
							int sensitivity_ordering_type)
{
		
	target_ = target;
		
	localValue_ = local_value;
    lowerBound_ = lower_value;
    upperBound_ = upper_value;
	
	if (type == 0){
	    Type_ = "local";
	}
	else if (type == 1){
	    Type_ = "global";
	}
	else if (type == 2){
	    Type_ = "region";
	}
	else {
		std::cout << "Wrong type of postprocessing. Avaialble are: Global | Local | Region" << std::endl;
	    exit(-1);
	}

	if (postprocessorType_ == "sensitivity") {
		if (sensitivity_ordering_type == 0) {
			orderingType_ = "peakvalues";
		}
		else if (sensitivity_ordering_type == 1) {
			orderingType_ = "area";
		}
		else if (sensitivity_ordering_type == 2) {
			orderingType_ = "absolutearea";
		}
		else {
			std::cout << "Wrong ordering type. Avaialble are: PeakValues | Area | Absolute Area" << std::endl;
			exit(-1);
		}

		if (sensitivity_normalization_type == 0) {
			normalizationType_ = "local";
		}
		else if (sensitivity_normalization_type == 1) {
			normalizationType_ = "maxvalue";
		}
		else {
			std::cout << "Wrong normalization type. Avaialble are: Local | Max Value" << std::endl;
			exit(-1);
		}
	}
}

void PostProcessor::PrepareFlux(std::string specie, std::string element, int type, double local_value,int thickness, 
			bool thicknesslogscale, int labeltype, int depth, int width, double threshold)
{
	species_ = specie;
	element_ = element;

	islogscale = thicknesslogscale;
	depth_ = depth;
	width_ = width;
	threshold_ = threshold;

	localValue_ = local_value;
    lowerBound_ = 0;
    upperBound_ = 0;

	if(thickness == 0) // absolute
	{
		thickness_ = "absolute";
	}
	else if(thickness == 1) // relative (%)
	{
		thickness_ = "relative";
	}
	else
	{
		std::cout << "Wrong thickness type. Avaialble are: Absolute | Relative(%)" << std::endl;
		exit(-1);
	}

	if(labeltype == 0) // absolute
	{
		labeltype_ = "absolute";
	}
	else if(labeltype == 1) // relative (%) 
	{
		labeltype_ = "relative";
	}
	else
	{
		std::cout << "Wrong labelling type. Avaialble are: Absolute | Relative(%)" << std::endl;
		exit(-1);
	}

	if(type == 0)
	{
		Type_ = "destruction";
	}
	else if(type == 1)
	{
		Type_ = "production";
	}
	else
	{
		std::cout << "Wrong FluxAnalysis type. Avaialble are: Production | Destruction" << std::endl;
		exit(-1);
	}
}

int PostProcessor::ComputeROPAPython(double* coefficients, int* reactions, int len)
{
    ROPA* widget;
    widget = new ROPA(kineticFolder_, outputFolder_, Type_, target_, localValue_, lowerBound_, upperBound_);
	data_->ReadFileResults(outputFolder_);
	data_->ReadKineticMechanism(kineticFolder_);
	widget->SetDatabase(data_);
    return widget->ROPA_Calculations_Python(coefficients, reactions, len);
}

int PostProcessor::ComputeSensitivityPython(double* coefficients, int* reactions, int len) 
{
	Sensitivities* widget;
	widget = new Sensitivities(normalizationType_, Type_, orderingType_, target_, localValue_, lowerBound_, upperBound_);
	data_->ReadFileResults(outputFolder_);
	data_->ReadKineticMechanism(kineticFolder_);
	widget->SetDatabase(data_);
	widget->Prepare();
	widget->ReadSensitvityCoefficients();
	return widget->Sensitivities_Python_PostProcessing(coefficients, reactions, len);

	return 0;
}

int PostProcessor::ComputeFluxPython(int* indexFirstName, int* indexSecondName, double* computedThickness, double* computedLabel, int* lenght)
{
	ROPA* widget;
    widget = new ROPA(kineticFolder_, outputFolder_, "local", species_, localValue_, lowerBound_, upperBound_);
	data_->ReadFileResults(outputFolder_);
	data_->ReadKineticMechanism(kineticFolder_);
	widget->SetDatabase(data_);
	return widget->FluxAnalysis(element_,thickness_, Type_, labeltype_,depth_,width_,threshold_, islogscale, 
						indexFirstName, indexSecondName, computedThickness, computedLabel, lenght);
	
}

int PostProcessor::GiveMeReactionRate(int reaction_index, double* reaction_rate)
{
	ROPA* widget;
    widget = new ROPA(kineticFolder_, outputFolder_, "global", "H2", 0, 0, 0);
	
	data_->ReadFileResults(outputFolder_);
	data_->ReadKineticMechanism(kineticFolder_);
	widget->SetDatabase(data_);

	return widget->GetReactionRates(reaction_index, reaction_rate);
}

int PostProcessor::GiveMeFormationRate(std::string specie, std::string units, 
									std::string type, double* formation_rate)
{
	ROPA* widget;
    widget = new ROPA(kineticFolder_, outputFolder_, "global", "H2", 0, 0, 0);
	
	data_->ReadFileResults(outputFolder_);
	data_->ReadKineticMechanism(kineticFolder_);
	widget->SetDatabase(data_);

	return widget->GetFormationRates(specie, units, type, formation_rate);
}

int PostProcessor::GiveMeSensitivityCoefficient(std::string normalization_type, std::string target, double* coefficient, int reaction_index)
{
	Type_ = "global";
	orderingType_ = "peakvalues";
	normalizationType_ = normalization_type;
	target_ = target;
	localValue_ = 0;
	lowerBound_ = 0;
	upperBound_ = 0;
	
	Sensitivities* widget;
	widget = new Sensitivities(normalizationType_, Type_, orderingType_, target_, localValue_, lowerBound_, upperBound_);
	
	data_->ReadFileResults(outputFolder_);
	data_->ReadKineticMechanism(kineticFolder_);
	widget->SetDatabase(data_);
	widget->Prepare();
	widget->ReadSensitvityCoefficients();

	return widget->GetSensitivityProfile(reaction_index, coefficient);
}