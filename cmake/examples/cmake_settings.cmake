return {
  build_dir = "/Users/tdinelli/Documents/GitHub/pySMOKEPostProcessor/build/${variant:buildType}",
  build_options = {},
  env = {},
  generate_options = { "-D CMAKE_CXX_COMPILER:PATH=/opt/homebrew/opt/llvm/bin/clang++", "-D CMAKE_EXPORT_COMPILE_COMMANDS:BOOL=TRUE", "-D Eigen3_DIR:PATH=/Users/tdinelli/NumericalLibraries/eigen/eigen-3.4.0/share/eigen3/cmake", "-D Boost_ROOT:PATH=/Users/tdinelli/NumericalLibraries/boost/boost-1.83.0-clang-17.0.1" },
  working_dir = "${dir.binary}"
}

return {
  build_dir = "/Users/tdinelli/Documents/GitHub/pySMOKEPostProcessor/build/${variant:buildType}",
  build_options = {},
  env = {},
  generate_options = { "-DCMAKE_CXX_COMPILER:PATH=/opt/homebrew/bin/g++-13", "-DCMAKE_EXPORT_COMPILE_COMMANDS:BOOL=TRUE", "-DEigen3_DIR:PATH=/Users/tdinelli/NumericalLibraries/eigen/eigen-3.4.0/share/eigen3/cmake", "-DBoost_ROOT:PATH=/Users/tdinelli/NumericalLibraries/boost/boost-1.83.0-gcc-13.2.0" },
  working_dir = "${dir.binary}"
}
