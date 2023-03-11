#include "c_interface.h"
#include "c_utilities.h"

using namespace PostProcessor;

extern "C"
{

    void SensitivityAnalysis(char* kineticFolder,
                            char* outputFolder,
                            char* target,
                            char* sensitivity_type,
                            char* ordering_type,
                            char* normalization_type,
                            double sensitivity_local_value,
                            double sensitivity_region_lower_value,
                            double sensitivity_region_upper_value,
                            int len,
                            double* coefficients,
                            int* reactions)
    {
        try
        {
            ProfilesDatabase *data_;
            data_ = new ProfilesDatabase();
        
            Sensitivities* widget;
            widget = new Sensitivities();

            data_->ReadFileResults(outputFolder);
            data_->ReadKineticMechanism(kineticFolder);
            
            widget->SetDatabase(data_);
            widget->SetSensitivityType(sensitivity_type);
            widget->SetOrderingType(ordering_type);
            widget->SetNormalizationType(normalization_type);
            widget->SetTarget(target);
            widget->SetLocalValue(sensitivity_local_value);
            widget->SetLowerBound(sensitivity_region_lower_value);
            widget->SetUpperBound(sensitivity_region_upper_value);
            widget->Prepare();
            widget->ReadSensitvityCoefficients();

            widget->Sensitivity_Analysis(coefficients, reactions, len);
        }
        catch(const Exception &e)
        {
            set_error_string(e.what());
        } 
    }

    void RateOfProductionAnalysis( char* kineticFolder,
                                char* outputFolder,
                                char* species,
                                char* ropa_type,
                                double ropa_local_value,
                                double ropa_region_lower_value,
                                double ropa_region_upper_value,
                                int len,
                                double* coefficients,
                                int* reactions)
    {
        try
        {
            ProfilesDatabase *data_;
            data_ = new ProfilesDatabase();
        
            ROPA* widget;
            widget = new ROPA();

            data_->ReadFileResults(outputFolder);
            data_->ReadKineticMechanism(kineticFolder);
            widget->SetDatabase(data_);

            widget->SetROPAType(ropa_type);
            widget->SetSpecies(species);
            widget->SetLocalValue(ropa_local_value);
            widget->SetLowerBound(ropa_region_lower_value);
            widget->SetUpperBound(ropa_region_upper_value);

            widget->RateOfProductionAnalysis(coefficients, reactions, len);

        }
        catch(const Exception &e)
        {
            set_error_string(e.what());
        }  
    }
    
    void FluxAnalysis ( char* kineticFolder, 
                    char* outputFolder, 
                    char* species, 
                    char* element, 
                    char* type,
                    double local_value,
                    char* thickness,
                    bool* thicknesslogscale,
                    char* labeltype,
                    int depth,
                    int width,
                    double threshold,
                    int* indexFirstName,
                    int* indexSecondName,
                    double* computedThickness,
                    double* computedLabel,
                    int* lenght)
    {
        try
        {
            ProfilesDatabase *data_;
            data_ = new ProfilesDatabase();
        
            ROPA* widget;
            widget = new ROPA();

            data_->ReadFileResults(outputFolder);
            data_->ReadKineticMechanism(kineticFolder);

            widget->SetDatabase(data_);
            widget->SetSpecies(species);
            widget->SetElement(element);
            widget->SetFluxAnalysisType(type);
            widget->SetLocalValue(local_value);
            widget->SetThickness(thickness);
            widget->SetThicknessLogScale(thicknesslogscale);
            widget->SetLabelType(labeltype);
            widget->SetDepth(depth);
            widget->SetWidth(width);
            widget->SetThreshold(threshold);

            widget->FluxAnalysis(indexFirstName, indexSecondName, 
                                computedThickness, computedLabel, lenght);
        }
        catch(const Exception &e)
        {
            set_error_string(e.what());
        } 
    }
    void GetFormationRates ( char* kineticFolder, 
                            char* outputFolder, 
                            char* species, 
                            char* units, 
                            char* type, 
                            double* formation_rate)
    {
        try
        {
            // TODO Handling errorss
            ProfilesDatabase *data_;
            data_ = new ProfilesDatabase();
        
            ROPA* widget;
            widget = new ROPA();
        
            data_->ReadFileResults(outputFolder);
            data_->ReadKineticMechanism(kineticFolder);
            widget->SetDatabase(data_);
            widget->GetFormationRates(species, units, type, formation_rate);
        }
        catch(const Exception &e)
        {
            set_error_string(e.what());
        }
    }

    void GetReactionRates ( char* kineticFolder, 
                        char* outputFolder, 
                        int reaction_index, 
                        double* reaction_rate)
    {
        try
        {
            // TODO Handling errorss
            ProfilesDatabase *data_;
            data_ = new ProfilesDatabase();
        
            ROPA* widget;
            widget = new ROPA();
        
            data_->ReadFileResults(outputFolder);
            data_->ReadKineticMechanism(kineticFolder);
            widget->SetDatabase(data_);
            widget->GetReactionRates(reaction_index, reaction_rate);
        }
        catch(const Exception &e)
        {
            set_error_string(e.what());
        }
    }

    void GetSensitivityCoefficients(char* kineticFolder, 
                                    char* outputFolder, 
                                    int reaction_index, 
                                    char* target, 
                                    char* normalization_type, 
                                    double* sensitivity_coefficients)
    {
        try
        {
            ProfilesDatabase *data_;
            data_ = new ProfilesDatabase();
        
            Sensitivities* widget;
            widget = new Sensitivities();
        
            data_->ReadFileResults(outputFolder);
            data_->ReadKineticMechanism(kineticFolder);
            widget->SetDatabase(data_);
            widget->SetSensitivityType("global");
            widget->SetOrderingType("peak-values");
            widget->SetNormalizationType(normalization_type);
            widget->SetTarget(target);
            widget->SetLocalValue(0.);
            widget->SetLowerBound(0.);
            widget->SetUpperBound(0.);
            widget->Prepare();
            widget->ReadSensitvityCoefficients();

            widget->GetSensitivityProfile(reaction_index, sensitivity_coefficients);
        }
        catch(const Exception &e)
        {
            set_error_string(e.what());
        }
    }

    void BoundaryLimits( char* kineticFolder, 
	                    char* outputFolder,
	                    double* maximum_domain,
	                    double* minimum_domain,
                	    double* middle_domain)
    {
        try
        {
            ProfilesDatabase* data_;
	        data_ = new ProfilesDatabase();
	        data_->ReadFileResults(outputFolder);
	        data_->ReadKineticMechanism(kineticFolder);

	        double maximum = data_->additional[0][data_->number_of_abscissas_ - 1];
	        double minimum = data_->additional[0][0];
	        double middle = 0.50*(data_->additional[0][0]+data_->additional[0][data_->number_of_abscissas_-1]);

	        for (int i = 0; i < 1; i++)
	        {
		        maximum_domain[i] = maximum;
		        minimum_domain[i] = minimum;
		        middle_domain[i] = middle;
	        }
        }
        catch(const Exception &e)
        {
            set_error_string(e.what());
        }
    }
    
    int postprocessor_get_error()
    {        
        int temp = PostProcessor::postprocessor_last_func_call_error;
        PostProcessor::postprocessor_last_func_call_error = 0;
        return temp;
    }

    const char *postprocessor_get_error_string()
    {
        return PostProcessor::postprocessor_error_string;
    }   
} // extern "C"