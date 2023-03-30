
#include "c_utilities.h"
namespace PostProcessor
{

// 1 if the last function call caused an error, 0 else
int postprocessor_last_func_call_error = 0;

const char *postprocessor_error_string = "No error.";

void set_error_string(const char *new_error_string)
{
    postprocessor_error_string = new_error_string;
    postprocessor_last_func_call_error = 1;
}

} // namespace SPLINTER
