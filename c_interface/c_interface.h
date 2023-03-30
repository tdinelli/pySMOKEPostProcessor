#ifndef OPENSMOKE_POSTPROCESSOR_CINTERFACE_H
#define OPENSMOKE_POSTPROCESSOR_CINTERFACE_H

#include "definitions.h"

#include "source/PostProcessorFluxMap.h"
#include "source/ProfilesDatabase.h"
#include "source/Sensitivities.h"
#include "source/ROPA.h"

#ifdef __cplusplus
    extern "C" 
    {
#endif

POSTPROCESSOR_API void GetSensitivityCoefficients( char* kineticFolder, 
                                                char* outputFolder, 
                                                int reaction_index, 
                                                char* target, 
                                                char* normalization_type, 
                                                double* sensitivity_coefficients);

POSTPROCESSOR_API void GetFormationRates ( char* kineticFolder, 
                                        char* outputFolder, 
                                        char* species, 
                                        char* units, 
                                        char* type, 
                                        double* formation_rate);

POSTPROCESSOR_API void GetReactionRates ( char* kineticFolder, 
                                        char* outputFolder, 
                                        int reaction_index, 
                                        double* reaction_rate);

POSTPROCESSOR_API void FluxAnalysis (char* kineticFolder, 
                                    char* outputFolder, 
                                    char* species, 
                                    char* element, 
                                    char* type,
                                    double local_value,
                                    char* thickness, // 0-absolute 1-relative(%)
                                    bool thicknesslogscale,
                                    char* labeltype, // 0-absolute 1-relative(%)
                                    int depth,
                                    int width,
                                    double threshold,
                                    int* indexFirstName,
                                    int* indexSecondName,
                                    double* computedThickness,
                                    double* computedLabel,
                                    int* lenght);

POSTPROCESSOR_API void SensitivityAnalysis(char* kineticFolder,
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
                                    int* reactions);

POSTPROCESSOR_API void RateOfProductionAnalysis( char* kineticFolder,
                                            char* outputFolder,
                                            char* species,
                                            char* ropa_type,
                                            double ropa_local_value,
                                            double ropa_region_lower_value,
                                            double ropa_region_upper_value,
                                            int len,
                                            double* coefficients,
                                            int* reactions);

POSTPROCESSOR_API void BoundaryLimits( char* kineticFolder, 
                                    char* outputFolder,
                                    double* maximum_domain,
                                    double* minimum_domain,
                                    double* middle_domain);

/**
 * Check if the last library call resulted in an error.
 * Will reset upon call, so two consecutive calls to this function may not return the same value.
 *
 * @return 1 if error, 0 else.
 */
POSTPROCESSOR_API int postprocessor_get_error();

/**
 * Get a string describing the error.
 *
 * @return Error string.
 */
POSTPROCESSOR_API const char *postprocessor_get_error_string();

#ifdef __cplusplus
    }
#endif

#endif // OPENSMOKE_POSTPROCESSOR_CINTERFACE_H