#!/usr/bin/env python
import os
import subprocess
import platform

platofrmName = platform.system()

platofrmToTemporaryDirDictionary = {
  'Linux':'/tmp/legilibere/',
  'Darwin':'somewhere not in tmp because tmp is deleted on restart',
  'Windows':'ok, It is your choice :)'}

tmpDir = platofrmToTemporaryDirDictionary.get(platofrmName)
if tmpDir is None:
    print("Your platform is " + platofrmName + " and you do not have a temporary dir selected.")

if not os.path.exists(tmpDir):
    os.makedirs(tmpDir)
    print('The work directory did not exist so I created it')
    print(tmpDir)
    
subprocess.check_call(["./1_clrro_import_download_pages.py", tmpDir])
