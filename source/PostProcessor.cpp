/*-----------------------------------------------------------------------*\
|    ___                   ____  __  __  ___  _  _______                  |
|   / _ \ _ __   ___ _ __ / ___||  \/  |/ _ \| |/ / ____| _     _         |
|  | | | | '_ \ / _ \ '_ \\___ \| |\/| | | | | ' /|  _| _| |_ _| |_       |
|  | |_| | |_) |  __/ | | |___) | |  | | |_| | . \| |__|_   _|_   _|      |
|   \___/| .__/ \___|_| |_|____/|_|  |_|\___/|_|\_\_____||_|   |_|        |
|        |_|                                                              |
|                                                                         |
|   Author: Alberto Cuoci <alberto.cuoci@polimi.it>                       |
|   CRECK Modeling Group <http://creckmodeling.chem.polimi.it>            |
|   Department of Chemistry, Materials and Chemical Engineering           |
|   Politecnico di Milano                                                 |
|   P.zza Leonardo da Vinci 32, 20133 Milano                              |
|																		  |
|   This file has been modified from the original OpenSMOKE postprocessor |
|	to adapt it in python.                                                |
|																		  |
|   Authors: Timoteo Dinelli <timoteo.dinelli@polimi.it>                  |
|			 Edoardo Ramalli <edoardo.ramalli@polimi.it>                  |
\*-----------------------------------------------------------------------*/

#include "PostProcessor.h"
#include "ROPA.h"
#include "Sensitivities.h"

// Global
PostProcessor::PostProcessor(std::string postporcessorType, std::string kineticFolder, std::string outputFolder)
{
	data_ = new ProfilesDatabase();
	postprocessorType_ = postporcessorType;
	kineticFolder_ = kineticFolder;
	outputFolder_ = outputFolder;
}

PostProcessor::~PostProcessor()
{
}

void PostProcessor::Prepare()
{	
	if (postprocessorType_ == "ropa") 
	{
		std::cout << " Plese insert which kind of ROPA do you want to compute: " << std::endl;
		std::cin >> ropaType_;
		std::cout << " Plese insert the specie you want to compute the ropa: " << std::endl;
		std::cin >> species_;
		std::cout << "-----------------------------------------------------------------------------" << std::endl;
		
		std::cout.setstate(std::ios_base::failbit);
		
		if (data_->ReadFileResults(outputFolder_) == true)
		{
			std::cout.clear();
			std::cout << " Output read OK!" << std::endl;
		}
		else 
		{
			std::cout.clear();
			std::cout << " ERROR: Provide a valid directory for the output folder" << std::endl;
			exit(-1);
		}
		
		std::cout.setstate(std::ios_base::failbit);
		
		if (data_->ReadKineticMechanism(kineticFolder_) == true) 
		{
			std::cout.clear();
			std::cout << " Kinetic Mechanism read OK!" << std::endl;
			std::cout << "-----------------------------------------------------------------------------" << std::endl;
		}
		else
		{
			std::cout.clear();
			std::cout << " ERROR: Provide a valid directory for the kineic mechanism folder" << std::endl;
			exit(-1);
		}
		
		std::cout.clear();
	}
	else if (postprocessorType_ == "sensitivity") 
	{
		std::cout << " Plese insert which kind of Sensitivity analysis do you want to compute: " << std::endl;
		std::cin >> sensitivityType_;
		std::cout << " Plese insert the specie you want to compute the ropa: " << std::endl;
		std::cin >> species_;
		std::cout << " Please insert which kind of normalization do you want: " << std::endl;
		std::cin >> normalizationType_;
		std::cout << " Please insert which kind of ordering do you want: " << std::endl;
		std::cin >> orderingType_;
		std::cout << "-----------------------------------------------------------------------------" << std::endl;

		std::cout.setstate(std::ios_base::failbit);

		if (data_->ReadFileResults(outputFolder_) == true)
		{
			std::cout.clear();
			std::cout << " Output read OK!" << std::endl;
		}
		else
		{
			std::cout.clear();
			std::cout << " ERROR: Provide a valid directory for the output folder" << std::endl;
			exit(-1);
		}

		std::cout.setstate(std::ios_base::failbit);

		if (data_->ReadKineticMechanism(kineticFolder_) == true)
		{
			std::cout.clear();
			std::cout << " Kinetic Mechanism read OK!" << std::endl;
			std::cout << "-----------------------------------------------------------------------------" << std::endl;
		}
		else
		{
			std::cout.clear();
			std::cout << " ERROR: Provide a valid directory for the kineic mechanism folder" << std::endl;
			exit(-1);
		}

		std::cout.clear();
	}

}

void PostProcessor::ComputeROPA()
{
    ROPA* widget;

	if (ropaType_ == "global") 
	{
		PrintRecap_ROPA();
		widget = new ROPA(kineticFolder_, outputFolder_, ropaType_, species_);
	}
	else if (ropaType_ == "local") 
	{
		std::cout << " Please insert the value for which you want to compute ropa:" << std::endl;
		std::cin >> localValue_;
		PrintRecap_ROPA();
		widget = new ROPA(kineticFolder_, outputFolder_, ropaType_, species_, localValue_);
	}
	else if (ropaType_ == "region") 
	{
		std::cout << " Please insert the value of the lower bound for which you want to compute ropa:" << std::endl;
		std::cin >> lowerBound_;
		std::cout << " Please insert the value of the upper bound for which you want to compute ropa:" << std::endl;
		std::cin >> upperBound_;
		PrintRecap_ROPA();
		widget = new ROPA(kineticFolder_, outputFolder_, ropaType_, species_, lowerBound_, upperBound_);
	}
	else 
	{
		std::cout << " Plese select one of the available type of ROPA: global | local | region" << std::endl;
		exit(-1);
	}

    widget->SetDatabase(data_);
    widget->ROPA_Calculations();
}

void PostProcessor::SensitivityAnalysis() 
{
	Sensitivities* widget;
	if (sensitivityType_ == "global")
	{
		PrintRecap_SENSITIVITY();
		widget = new Sensitivities(normalizationType_, sensitivityType_, orderingType_, species_);
	}
	else if (sensitivityType_ == "local")
	{
		std::cout << " Please insert the value for which you want to compute the sensitivity analysis:" << std::endl;
		std::cin >> localValue_;
		PrintRecap_SENSITIVITY();
		widget = new Sensitivities(normalizationType_, sensitivityType_, orderingType_, species_, localValue_);
	}
	else if (sensitivityType_ == "region")
	{
		std::cout << " Please insert the value of the lower bound for which you want to compute the sensitivity analysis:" << std::endl;
		std::cin >> lowerBound_;
		std::cout << " Please insert the value of the upper bound for which you want to compute the sensitivity analysis:" << std::endl;
		std::cin >> upperBound_;
		PrintRecap_SENSITIVITY();
		widget = new Sensitivities(normalizationType_, sensitivityType_, orderingType_, species_, lowerBound_, upperBound_);
	}
	else
	{
		std::cout << " Plese select one of the available type of Sensitivity Analysis: global | local | region" << std::endl;
		exit(-1);
	}

	widget->SetDatabase(data_);
	widget->Prepare();
	widget->ReadSensitvityCoefficients();
	widget->Sensitivities_PostProcessing();
}

void PostProcessor::PrintRecap_ROPA() 
{
	std::cout << "-----------------------------------------------------------------------------" << std::endl;
	std::cout << "Computing Rate of production analysis for" << std::endl;
	std::cout << "  *kinetic mechanism:  " << kineticFolder_ << std::endl;
	std::cout << "  *simulation results: " << outputFolder_ << std::endl;
	std::cout << "  *selected species:   " << species_ << std::endl;
	std::cout << "  *ROPA type:          " << ropaType_ << std::endl;
	if (ropaType_ == "local") 
	{
		std::cout << "  *local Value:        " << localValue_ << std::endl;
	}
	if (ropaType_ == "region") 
	{
		std::cout << "  *lower bound Value:  " << lowerBound_ << std::endl;
		std::cout << "  *upper bound Value:  " << upperBound_ << std::endl;
	}
	std::cout << "-----------------------------------------------------------------------------" << std::endl;
}

void PostProcessor::PrintRecap_SENSITIVITY()
{
	std::cout << "-----------------------------------------------------------------------------" << std::endl;
	std::cout << "Computing Rate of production analysis for" << std::endl;
	std::cout << "  *kinetic mechanism:  " << kineticFolder_ << std::endl;
	std::cout << "  *simulation results: " << outputFolder_ << std::endl;
	std::cout << "  *selected species:   " << species_ << std::endl;
	std::cout << "  *Sensitivity type:   " << sensitivityType_ << std::endl;
	if (sensitivityType_ == "local")
	{
		std::cout << "  *local Value:        " << localValue_ << std::endl;
	}
	if (sensitivityType_ == "region")
	{
		std::cout << "  *lower bound Value:  " << lowerBound_ << std::endl;
		std::cout << "  *upper bound Value:  " << upperBound_ << std::endl;
	}
	std::cout << "  *Normalization type: " << normalizationType_ << std::endl;
	std::cout << "  *Ordering type:      " << orderingType_ << std::endl;
	std::cout << "-----------------------------------------------------------------------------" << std::endl;
}
