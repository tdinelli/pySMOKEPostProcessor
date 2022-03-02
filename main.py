from ctypes import c_int, c_double, c_void_p, c_char_p, byref, cdll

path = '/Users/edoardo/Library/Mobile Documents/com~apple~CloudDocs/Projects/pyPostProcessor/source/edo.o'

kineticFolder = b"/Users/edoardo/Library/Mobile Documents/com~apple~CloudDocs/Projects/sciexpem/ChemModels/26"
outputFolder = b"/Users/edoardo/Desktop/Case0"
specie = b"H2"

c_library = cdll.LoadLibrary(path)

c_library.pyPostProcessor.argtypes = [c_char_p,
                                      c_char_p,
                                      c_char_p,
                                      c_int,
                                      c_int,
                                      c_double,
                                      c_double,
                                      c_double,
                                      c_void_p,
                                      c_void_p,
                                      c_int]

c_library.pyPostProcessor.restype = c_int
n = 10

coefficients = (c_double * n)()
reactions = (c_int * n)()

print('edooo')

code = c_library.pyPostProcessor(c_char_p(kineticFolder),
                                 c_char_p(outputFolder),
                                 c_char_p(specie),
                                 c_int(0),
                                 c_int(1),
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
