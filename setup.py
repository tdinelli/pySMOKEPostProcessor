import setuptools
import os

version_file_name = 'pySMOKEPostProcessor/version'  # Name of the file where the C++ back-end version is written
interface_package_name = 'pySMOKEPostProcessor'  # Both the name of the project and the name of the package
library_files_dir_name = 'lib'  # Path to the compiled library files

with open("README.md", "r") as fh:
    long_description = fh.read()
    
with open(version_file_name, "r") as fv:
    version = fv.read()
    
# Get the absolute path of the directory containing this file
setup_py_dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(setup_py_dir_path)  # In case this script is being run from another directory
pysmokepostprocessor_python_interface_path = os.path.join(setup_py_dir_path, interface_package_name)

version_file_path = os.path.join(setup_py_dir_path, version_file_name)
library_files_dir_path = os.path.join(setup_py_dir_path, interface_package_name, library_files_dir_name)

# Verify that the library has been built
# If these files don't exist, it means that the `make install` step hasn't been run.
if not (os.path.exists(version_file_path) and os.path.exists(library_files_dir_path)):
    print("Error: It seems that pysmokepostprocessor has not been built.\n\n"
          + "Please note that to install the Python interface of pysmokepostprocessor from source,\n"
          + "you first need to build the library. See the guide at TODO for more information.")
    exit(1)

def get_available_backends(lib_path):
    """
    Gets a list of the available back-ends by looking into the lib directory.
    If there is at least one file in the directory that is supposed to contain a library file, this function
    assumes that the library is available.
    :param lib_path: Path to the lib directory
    :return: List of tuples: [(os, architecture), ...]
    """
    lib_versions_available = []
    for operating_system in os.listdir(lib_path):
        operating_system_path = os.path.join(library_files_dir_path, operating_system)
        if os.path.isdir(operating_system_path):
            for arch in os.listdir(os.path.join(lib_path, operating_system)):
                arch_path = os.path.join(operating_system_path, arch)
                if os.path.isdir(arch_path):
                    lib_versions_available.append((operating_system, arch))
    return lib_versions_available

def get_backend_binary_path(lib_path, operating_system, arch):
    dir_path = os.path.join(lib_path, operating_system, arch)
    files = os.listdir(dir_path)
    # Shouldn't be more than one file per directory
    return os.path.join(dir_path, files[0])

# Make sure all required files will be installed by adding them to the package data list
# Add version file to the package data list
package_data = [version_file_path]
# Add all available library files to the package data list
for operating_system, arch in get_available_backends(library_files_dir_path):
    package_data.append(get_backend_binary_path(library_files_dir_path, operating_system, arch))

setuptools.setup(
    name="pySMOKEPostProcessor",
	version = version,
	author='Timoteo Dinelli',
	author_email= 'timoteo.dinelli@polimi.it',
	description='Python Binder of the OpenSMOKE post processor',
	long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Titodinelli/pySMOKEPostProcessor",
	packages=setuptools.find_packages(exclude=['__pycache__']),
	install_requires=['numpy', 'pandas', 'matplotlib', 'networkx', 'pydot', 'graphviz', 'scipy', 'jupyter'],
	package_data={interface_package_name: package_data},
	classifiers=[
		"Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Chemical Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
	],
    
	include_package_data=True,
)

'''
$ python setup.py bdist_wheel
'''
