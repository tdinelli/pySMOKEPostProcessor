#include "c_interface.h"
#include "c_utilities.h"

extern "C" {
    void getBoundary( char* kineticFolder, 
	                char* outputFolder,
	                double* maximum_domain,
	                double* minimum_domain,
                	double* middle_domain)
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
} // extern "C"