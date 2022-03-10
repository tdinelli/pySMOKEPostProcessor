from ctypes import c_int, c_double, c_void_p, c_char_p, byref, cdll

# ROPA
# TITOOO

path = r'C:\Users\timot\Desktop\GitHub\pyPostProcessor\project\x64\Debug\pySMOKEpostprocessor.dll' 
kineticFolder = b"C:\\Users\\timot\\Desktop\\Example_ROPA_AMN\\TOT2110_soot_last"
outputFolder = b"C:\\Users\\timot\\Desktop\\Example_ROPA_AMN\\Sun2017_RCM_AMN\\output\\Case0"
specie = b"H2"

# EDOOOO

# path = '/Users/edoardo/Library/Mobile Documents/com~apple~CloudDocs/Projects/pyPostProcessor/source/pyPostProcessor.o'
# kineticFolder = b"/Users/edoardo/Library/Mobile Documents/com~apple~CloudDocs/Projects/sciexpem/ChemModels/26"
# outputFolder = b"/Users/edoardo/Desktop/Case0"

c_library = cdll.LoadLibrary(path)

c_library.pyROPAPostProcessor.argtypes = [c_char_p, # kinetic folder
                                          c_char_p, # output folder
                                          c_char_p, # sepcie
                                          c_int,    # command
                                          c_int,    # ropa type 0: local | 1: global | 2: region
                                          c_double, # ropa local value
                                          c_double, # ropa region lower value
                                          c_double, # ropa region upper value
                                          c_void_p, # ropa coefficients
                                          c_void_p, # ropa reactions indices
                                          c_int]    # ropa number of reactions

c_library.pyROPAPostProcessor.restype = c_int

n = 20

coefficients = (c_double * n)()
reactions = (c_int * n)()

code = c_library.pyROPAPostProcessor(c_char_p(kineticFolder), # kinetic folder
                                    c_char_p(outputFolder),   # output folder
                                    c_char_p(specie),         # specie
                                    c_int(0),                 # command (to be removed)
                                    c_int(1),                 # ropa type 0: local | 1:global | 2: region
                                    c_double(0),              # ropa local value
                                    c_double(0),              # ropa region lower value 
                                    c_double(0),              # ropa region upper value
                                    byref(coefficients),      # ropa coefficients
                                    byref(reactions),         # ropa reactions indices
                                    c_int(n))                 # ropa number of reactions

print (code)

coefficients = [c for c in coefficients]
reactions = [r for r in reactions]

print(coefficients)
print(reactions)

# g++ --std=c++17 -I /usr/local/include/eigen3 -I /Users/edoardo/Desktop/source -I /usr/local/Cellar/boost/1.78.0/include -L /usr/local/Cellar/boost/1.78.0/lib -lboost_filesystem main.cpp CollectionOfClasses.cpp PostProcessor.cpp -o pyPostProcessor.o -O3 -Wall -DNDEBUG -shared -fPIC -w
