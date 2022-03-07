from ctypes import c_int, c_double, c_void_p, c_char_p, byref, cdll

path = '/Users/edoardo/Library/Mobile Documents/com~apple~CloudDocs/Projects/pyPostProcessor/source/pyPostProcessor.o'

kineticFolder = b"/Users/edoardo/Downloads"
outputFolder = b"/Users/edoardo/Downloads"
specie = b"HE"

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


# g++ --std=c++17 -I /usr/local/include/eigen3 -I /Users/edoardo/Desktop/source -I /usr/local/Cellar/boost/1.78.0/include -L /usr/local/Cellar/boost/1.78.0/lib -lboost_filesystem main.cpp CollectionOfClasses.cpp PostProcessor.cpp -o pyPostProcessor.o -O3 -Wall -DNDEBUG -shared -fPIC -w
