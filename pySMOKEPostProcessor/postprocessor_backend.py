import os
import ctypes
import platform
import typing as ty

from .utilities import get_py_string, out, get_architecture

class PostProcessorBackend:
    def __init__(self):
        # Handle to the cdll instance
        self._handle = None

        full_path = os.path.realpath(__file__)  # Path to this file
        postprocessor_python_main_dir = os.path.dirname(full_path)

        # Locate version file. If we cannot find it then we won't be able to find splinter either
        version_file = os.path.join(postprocessor_python_main_dir, "version")
        if not os.path.exists(version_file):
            raise Exception(
                "Missing version file in pySMOKEPostProcessor directory! "
                "Please notify the developers of pySMOKEPostProcessor of this error."
            )

        with open(version_file) as f:
            postprocessor_version = f.read().strip()
        self.version = postprocessor_version

    def is_loaded(self) -> bool:
        """
        Check if the back-end of Post Processor has been loaded
        :return:
        """
        return self._handle is not None

    def load(self, lib_file: str=None) -> bool:
        """
        Attempt to load the shared library back-end from the file in lib_file. If lib_file is None,
        then we will try to automatically locate it.

        Raises FileNotFoundError if we were unable to find the library automatically, or if lib_file does not exist.
        Raises
        :param lib_file: Path to attempt to load pySMOKEPostProcessor from.
        :return: True if pySMOKEPostProcessor was loaded, False otherwise
        """
        if self.is_loaded():
            return True

        if lib_file is None:
            lib_file = self._locate_postprocessor()
            if lib_file is None:
                raise FileNotFoundError(
                    "Unable to automatically locate pySMOKEPostProcessor.\n"
                    "It is possible that pySMOKEPostProcessor was not compiled for the operating system and architecture you are "
                    "using. If that is the case, you can compile pySMOKEPostProcessor yourself and load it using "
                    "'pysmokepostprocessor.load(\"/path/to/libpySMOKEPostProcessor.so\")'"
                )
        else:
            if not os.path.exists(lib_file):
                raise FileNotFoundError(
                    "Unable to load pySMOKEPostProcessor from {}: File does not exist!".format(lib_file)
                )

        try:
            self._handle = ctypes.cdll.LoadLibrary(lib_file)
            self._set_function_signatures()

        except Exception as e:
            out("Error:")
            out("Either you are trying to load a library with another architecture (32bit/64bit) ")
            out("than the Python you are using, ", True)
            out("or the file you are trying to load ({}) could not be found.".format(lib_file))
            out("For reference your Python is " + str(8*ctypes.sizeof(ctypes.c_void_p)) + "bit.")
            out("Here is the error message:")
            out(str(e))
            self._handle = None

    @property
    def handle(self):
        """
        Get the handle to the cdll instance.
        Raises Exception if the pySMOKEPostProcessor back-end has not been loaded.
        :return:
        """
        if self._handle is None:
            raise Exception("The pySMOKEPostProcessor back-end has not been loaded!\n"
                    + "You can do it with pysmokepostprocessor.load(\"/path/to/libpySMOKEPostProcessor-x-y.so\")")
        return self._handle

    def call(self, function, *args):
        """
        Make a call to the C++ back-end
        :param function: What function to call
        :param args: Arguments to the function
        :return: Return value of the function
        """
        res = function(*args)

        if self.handle.postprocessor_get_error():
            # TODO: Sometimes the string is correct, sometimes not. Investigate.
            errorMsg = get_py_string(self.handle.postprocessor_get_error_string())
            raise Exception("Got exception when calling {}: {}".format(function.__name__, errorMsg))

        return res

    # Set expected argument types and return types of all functions
    def _set_function_signatures(self):
        """
        Set the return types and argument types of all functions as declared in the C interface.
        :return:
        """
        # Define types for int* and double*
        c_int = ctypes.c_int
        c_double = ctypes.c_double
        c_void_p = ctypes.c_void_p
        c_char = ctypes.c_char
        c_char_p = ctypes.c_char_p

        c_int_p = ctypes.POINTER(c_int) # This has to be checkeddddd
        c_double_p = ctypes.POINTER(c_double)

        this = self

        def set_signature(function_name: str, return_type, *parameters):
            function = getattr(this._handle, function_name)

            setattr(function, 'restype', return_type)
            setattr(function, 'argtypes', list(parameters))

        set_signature('postprocessor_get_error', c_int)
        set_signature('postprocessor_get_error_string', c_char_p)
        set_signature('BoundaryLimits', c_void_p, c_char_p, c_char_p, c_double_p, c_double_p, c_double_p)

    def _locate_postprocessor(self) -> ty.Optional[str]:
        is_linux = platform.system() == 'Linux'
        is_windows = platform.system() == 'Windows'
        is_mac = platform.system() == 'Darwin'

        full_path = os.path.realpath(__file__)  # Path to this file
        postprocessor_python_main_dir = os.path.dirname(full_path)

        # postprocessor_basename = "pySMOKEPostProcessor-" + self.version
        postprocessor_basename = "pySMOKEPostProcessor"
        if is_linux:
            operating_system = "linux"
            postprocessor_name = "lib" + postprocessor_basename + ".so"
        elif is_windows:
            operating_system = "windows"
            postprocessor_name = postprocessor_basename + ".dll"
        elif is_mac:
            operating_system = "osx"
            postprocessor_name = "lib" + postprocessor_basename + ".dylib"
        else:
            raise "pySMOKEPostProcessor: Unknown platform: " + platform.system()

        #lib_postprocessor = os.path.join(postprocessor_python_main_dir, "lib", operating_system, get_architecture(), postprocessor_name)
        lib_postprocessor = "/Users/tdinelli/Documents/GitHub/pySMOKEPostProcessor/build/libpySMOKEPostProcessor.dylib"
        if os.path.exists(lib_postprocessor):
            return lib_postprocessor

        return None


postprocessor_backend_obj = PostProcessorBackend()
