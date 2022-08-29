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

void PostProcessor::Prepare(std::string specie, int type, double local_value, double lower_value, 
							double upper_value, int sensitivity_normalization_type, 
							int sensitivity_ordering_type)
{
		
	species_ = specie;
		
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
			exit(-1);
		}

		if (sensitivity_normalization_type == 0) {
			normalizationType_ = "local";
		}
		else if (sensitivity_normalization_type == 1) {
			normalizationType_ = "maxvalue";
		}
		else {
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
		exit(-1);
	}
}

int PostProcessor::ComputeROPAPython(double* coefficients, int* reactions, int len)
{
    ROPA* widget;
    widget = new ROPA(kineticFolder_, outputFolder_, Type_, species_, localValue_, lowerBound_, upperBound_);
	data_->ReadFileResults(outputFolder_);
	data_->ReadKineticMechanism(kineticFolder_);
	widget->SetDatabase(data_);
    return widget->ROPA_Calculations_Python(coefficients, reactions, len);
}

int PostProcessor::ComputeSensitivityPython(double* coefficients, int* reactions, int len) 
{
	Sensitivities* widget;
	widget = new Sensitivities(normalizationType_, Type_, orderingType_, species_, localValue_, lowerBound_, upperBound_);
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