from setuptools import setup, find_packages
import sys

sys.dont_write_bytecode = True

setup(
    name='qlikoauth',
    version='0.1.0',
    author='Rikard Braathen',
    packages=find_packages(),
    include_package_data=True,
    license='LICENSE.txt',
    install_requires=[
    "CherryPy == 3.2.5",
    "oauth2client >= 1.2.0",
    "requests",
],
)
