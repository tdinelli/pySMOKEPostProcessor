#ifndef OPENSMOKE_POSTPROCESSOR_CINTERFACE_H
#define OPENSMOKE_POSTPROCESSOR_CINTERFACE_H

#include "definitions.h"

// Pointer to C++ objects, passed into the C interface then cast to the correct type.
typedef void *postprocessor_obj_ptr;

#ifdef __cplusplus
    extern "C" 
    {
#endif

POSTPROCESSOR_API postprocessor_obj_ptr GetSensitivityCoefficient( char* kineticFolder, 
                                                                char* outputFolder, 
                                                                int* reaction_index, 
                                                                char* target, 
                                                                char* normalization_type, 
                                                                double* sensitivity_coefficient);

POSTPROCESSOR_API postprocessor_obj_ptr GetFormationRates ( char* kineticFolder, 
                                                        char* outputFolder, 
                                                        char* species, 
                                                        char* units, 
                                                        char* type, 
                                                        double* formation_rate);

POSTPROCESSOR_API postprocessor_obj_ptr GetReactionRates ( char* kineticFolder, 
                                                        char* outputFolder, 
                                                        int* reaction_index, 
                                                        double* reaction_rate);

POSTPROCESSOR_API postprocessor_obj_ptr FluxAnalysis ( char* kineticFolder, 
                                                    char* outputFolder, 
                                                    char* species, 
                                                    char* element, 
                                                    int* type, // 1-production 0-destruction
                                                    double* ropa_local_value,
                                                    int* thickness, // 0-absolute 1-relative(%)
                                                    bool* thicknesslogscale,
                                                    int* labeltype, // 0-absolute 1-relative(%)
                                                    int* depth,
                                                    int* width,
                                                    double* threshold,
                                                    int* indexFirstName,
                                                    int* indexSecondName,
                                                    double* computedThickness,
                                                    double* computedLabel,
                                                    int* lenght);

POSTPROCESSOR_API postprocessor_obj_ptr SensitivityAnalysis( char* kineticFolder,
                                                            char* outputFolder,
                                                            char* target,
                                                            int* sensitivity_type,
                                                            int* ordering_type,
                                                            int* normalization_type,
                                                            double* sensitivity_local_value,
                                                            double* sensitivity_region_lower_value,
                                                            double* sensitivity_region_upper_value,
                                                            double* coefficients,
                                                            int* reactions,
                                                            int* len);

POSTPROCESSOR_API postprocessor_obj_ptr RateOfProductionAnalysis( char* kineticFolder,
                                                                char* outputFolder,
                                                                char* specie,
                                                                int* ropa_type,
                                                                int* ordering_type,
                                                                int* normalization_type,
                                                                double* ropa_local_value,
                                                                double* ropa_region_lower_value,
                                                                double* ropa_region_upper_value,
                                                                double* coefficients,
                                                                int* reactions,
                                                                int* len);

POSTPROCESSOR_API postprocessor_obj_ptr BoundaryLimits( char* kineticFolder, 
                                                    char* outputFolder,
                                                    double* maximum_domain,
                                                    double* minimum_domain,
                                                    double* middle_domain);

#ifdef __cplusplus
    }
#endif

#endif // SPLINTER_CINTERFACE_H