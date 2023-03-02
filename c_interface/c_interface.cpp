#include "c_interface.h"
#include "c_utilities.h"

using namespace PostProcessor;

extern "C"
{
    void GetSensitivityCoefficient(char* kineticFolder, 
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

    void getBoundary( char* kineticFolder, 
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