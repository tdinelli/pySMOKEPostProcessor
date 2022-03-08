from ctypes import c_int, c_double, c_void_p, c_char_p, byref, cdll

# TITOOO

path = r'C:\Users\timot\Desktop\GitHub\pyPostProcessor\project\x64\Debug\pySMOKEpostprocessor.dll' 

# SENSITIVITA'
kineticFolder = b"C:\\Users\\timot\\OpenSMOKE++Suite\examples\\OpenSMOKEpp_BatchReactor\\04b-sensitivity-isothermal-constantpressure\\kinetics"
outputFolder = b"C:\\Users\\timot\\OpenSMOKE++Suite\\examples\\OpenSMOKEpp_BatchReactor\\04b-sensitivity-isothermal-constantpressure\\Output"
specie = b"H2"

c_library = cdll.LoadLibrary(path)

c_library.pySensitivityPostProcessor.argtypes = [c_char_p,
                                                c_char_p,
                                                c_char_p,
                                                c_int,
                                                c_int,
                                                c_int,
                                                c_int,
                                                c_double,
                                                c_double,
                                                c_double,
                                                c_void_p,
                                                c_void_p,
                                                c_int]

c_library.pySensitivityPostProcessor.restype = c_int
n = 10

coefficients = (c_double * n)()
reactions = (c_int * n)()


code = c_library.pySensitivityPostProcessor(c_char_p(kineticFolder),
                                 c_char_p(outputFolder),
                                 c_char_p(specie),
                                 c_int(0),
                                 c_int(1),
                                 c_int(0),
                                 c_int(0),
                                 c_double(0),
                                 c_double(0),
                                 c_double(0),
                                 byref(coefficients),
                                 byref(reactions),
                                 c_int(n))

print (code)

coefficients = [c for c in coefficients]
reactions = [r for r in reactions]

print(coefficients)
print(reactions)