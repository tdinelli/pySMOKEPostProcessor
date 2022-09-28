import setuptools

setuptools.setup(name='pySMOKEPostProcessor',
  version= '0.1.0',
  description='Python Binder of the OpenSMOKE post processor',
  author='Timoteo Dinelli',
  author_email= 'timoteo.dinelli@polimi.it',
  packages=setuptools.find_packages(),
  install_requires=['numpy', 'pandas', 'matplotlib', 'networkx', 'jupyter', 'pydot', 'graphviz', 'scipy'],
  keywords = ['Sensitivity Analysis', 'Elemental Flux Analysis', 'Rate Of Production', 'kinetics', 'opensmokepp'],
  include_package_data=True,
)

'''
$ python setup.py bdist_wheel
'''