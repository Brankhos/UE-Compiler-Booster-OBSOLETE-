import subprocess
import time
import sys
try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "-r", 'main_req.txt'])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "-r", 'requirements.txt'])
except Exception as E:
    print(E)
time.sleep(60)

