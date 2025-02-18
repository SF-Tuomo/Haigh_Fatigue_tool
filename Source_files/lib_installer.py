# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 09:14:44 2025

@author: SF Tuomo
"""

import subprocess
import sys
import importlib.util

def is_package_installed(package_name):
    # Check if the package is installed by attempting to find its spec
    return importlib.util.find_spec(package_name) is not None

def install_package(package):
    if not is_package_installed(package):
        print(f"{package} is not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    else:
        print(f"{package} is already installed.")

def install_packages(packages):
    for i in packages:
        install_package(i)


# Example usage:
# install_package('requests')  # Replace 'requests' with the package you want to check and install
