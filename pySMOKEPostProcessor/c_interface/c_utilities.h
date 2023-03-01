
#ifndef OPENSMOKE_POSTPROCESSOR_CUTILITIES_H
#define OPENSMOKE_POSTPROCESSOR_CUTILITIES_H

namespace PostProcessor
{

// Declare the global variables for use in all source files
// All extern variables are defined in cinterface/utilities.cpp
// Keep a list of objects so we avoid performing operations on objects that don't exist

extern int postprocessor_last_func_call_error; // Tracks the success of the last function call
extern const char *postprocessor_error_string; // Error string (if the last function call resulted in an error)

void set_error_string(const char *new_error_string);

} // namespace PostProcessor

#endif // OPENSMOKE_POSTPROCESSOR_CUTILITIES_H
