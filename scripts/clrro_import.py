import os
import subprocess

print("before")
print(os.getcwd())
subprocess.check_call(["./1_clrro_import_download_pages.py", "1"])
print("after")
