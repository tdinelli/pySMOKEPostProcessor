import os
import sys
import platform
import setuptools
import subprocess
from packaging import version


package_version = "0.4.0"
python_version = str(sys.version_info[0]) + str(sys.version_info[1])
os_system = platform.system().lower()
machine = platform.machine()
if os_system == 'darwin':
    library_name = 'pySMOKEPostProcessor.cpython-' + \
        python_version + '-' + os_system + '.so'
elif os_system == 'linux':
    library_name = 'pySMOKEPostProcessor.cpython-' + python_version + \
        '-' + machine + '-' + os_system + '-gnu' + '.so'
else:
    print("Unkown platform: {}. At the moment the code is tested only on MacOS and Linux".format(platform))
    exit(-1)

# Both the name of the project and the name of the package
interface_package_name = 'pySMOKEPostProcessor'

with open("README.md", "r") as fh:
    long_description = fh.read()

# Get the absolute path of the directory containing this file
setup_py_dir_path = os.path.dirname(os.path.realpath(__file__))

# In case this script is being run from another directory
os.chdir(setup_py_dir_path)
pysmokepostprocessor_python_interface_path = os.path.join(
    setup_py_dir_path, interface_package_name)


def get_cmake_version():
    output = subprocess.check_output(['cmake', '--version']).decode('utf-8')
    line = output.splitlines()[0]
    version = line.split()[2]
    return (version)


def build():
    cmake_version = version.parse(get_cmake_version())
    if cmake_version < version.parse("3.16.4"):
        print("Found cmake version {}, please update at least to 3.16.4".format(
            cmake_version))
        exit(1)
    elif cmake_version >= version.parse("3.16.4"):
        print(" * CMake found!")
    else:
        print("CMake not found in the system, please install CMake!")
        exit(1)
    # Create build directory
    interface_build_directory = os.path.join(setup_py_dir_path, "build")
    if os.path.exists(interface_build_directory):
        print("A build directory ({}) already exists please remove if you want to perform the automatic compilation".format(
            interface_build_directory))
    else:
        os.mkdir(interface_build_directory)

    # Build the project
    cmake_command = "export CXX=/opt/homebrew/bin/g++-13 && cmake -B {}".format(
        interface_build_directory)
    process = subprocess.Popen(
        cmake_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode('ascii')
    error = error.decode('ascii')
    if ("Error" in error):
        print(error)
        exit(-1)
    else:
        print(output)

    # Compile the interface
    cmake_command = "cmake --build {}".format(interface_build_directory)
    process = subprocess.Popen(
        cmake_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode('ascii')
    error = error.decode('ascii')
    if ("Error" in error):
        print(error)
        exit(-1)
    else:
        print(output)

    # Install the interface
    # Veramente brutto ma ci lavorerò
    cmake_command = "cd {} && make install && cd -".format(
        interface_build_directory)
    process = subprocess.Popen(
        cmake_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode('ascii')
    error = error.decode('ascii')
    if ("Error" in error):
        print(error)
        exit(-1)
    else:
        print(output)


# Verify that the library has been built
# If these files don't exist, it means that the `make install` step hasn't been run.
if not (os.path.exists(os.path.join(pysmokepostprocessor_python_interface_path, library_name))):
    print("WARNING: It seems that pysmokepostprocessor has not been built.\n"
          + " - An automatic attempt to build the library will be performed!\n"
          + " - Otherwise in case of failure note that you will need to build the C++ wrapper by hand")
    build()
elif (os.path.exists(os.path.join(pysmokepostprocessor_python_interface_path, library_name))):
    print("Found a compiled interface: {}. Remove it if you need to rebuild the C++ wrapper.".format(library_name))


setuptools.setup(
    name="pySMOKEPostProcessor",
    version=package_version,
    author='Timoteo Dinelli, Edoardo Ramalli, Luna Pratali Maffei, Andrea Nobili',
    author_email='timoteo.dinelli@polimi.it',
    description='Python Binder of the OpenSMOKE Graphical Post Processor',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Titodinelli/pySMOKEPostProcessor",
    packages=setuptools.find_packages(exclude=['__pycache__']),
    install_requires=['numpy', 'pandas', 'matplotlib',
                      'networkx', 'pydot', 'graphviz', 'scipy',],
    classifiers=[],
    package_data={'pySMOKEPostProcessor': [os.path.join(
        pysmokepostprocessor_python_interface_path, library_name)]},
    include_package_data=True,
)

'''
$ python setup.py bdist_wheel
'''
