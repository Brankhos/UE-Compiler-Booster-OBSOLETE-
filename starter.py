#! /usr/bin/python
import subprocess
import sys
from os.path import exists
import time
import os
venv_exists = exists("aavenv")
try:
    if not venv_exists:
        subprocess.check_call("pip install virtualenv".split(" "))
        subprocess.check_call("virtualenv venv --clear --download".split(" "))

except Exception as E:
    print(E)
    
curr_loc = os.getcwd()
venv_python_loc = f"{curr_loc}\\venv\\Scripts\\python.exe"

subprocess.check_call([venv_python_loc, "installer.py"])