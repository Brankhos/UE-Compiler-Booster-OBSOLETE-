#! /usr/bin/python
import subprocess
import sys
from os.path import exists
import time
import os
curr_loc = os.getcwd()
venv_python_loc = f"{curr_loc}\\venv\\Scripts\\python.exe"

try:
    if not exists("venv"):
        subprocess.check_call("pip install virtualenv".split(" "))
        subprocess.check_call("virtualenv venv --clear --download".split(" "))
        subprocess.check_call([venv_python_loc, "installer.py"])

except Exception as E:
    print(E)

subprocess.check_call([venv_python_loc, "main.py"])
