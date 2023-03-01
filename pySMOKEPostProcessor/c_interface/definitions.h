#ifndef POSTPROCESSOR_DEFINITIONS_H
#define POSTPROCESSOR_DEFINITIONS_H

#ifndef POSTPROCESSOR_API
# ifdef _MSC_VER
#  define POSTPROCESSOR_API __declspec(dllexport)
# else
#  define POSTPROCESSOR_API
# endif
#endif // POSTPROCESSOR_API

# include <exception>
# include <stdexcept>

namespace PostProcessor
{
    class Exception : public std::exception
    {
        private:
            std::string __what;

        public:

        Exception(const std::string& what) : __what(what){}

        const char* what() const throw()
        {
            return this->__what.c_str();
        }
    };
} // namespace Post Processor

#endif // POSTPROCESSOR_DEFINITIONS_H