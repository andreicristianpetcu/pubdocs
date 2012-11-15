#!/usr/bin/env python
import os
import subprocess
import platform

from os.path import expanduser
home = expanduser("~")

work_dir = home + '/tmp/legilibere/'

if not os.path.exists(work_dir):
    os.makedirs(work_dir)
    print('The work directory did not exist so I created it')
    print(work_dir)

clr_ro_dir = os.path.join(work_dir, 'clr_ro')

all_laws_dir = os.path.join(clr_ro_dir, 'all_laws')
all_laws_clean_dir = os.path.join(clr_ro_dir, 'all_laws_clean')

subprocess.check_call(["./1_clrro_fetch_laws_per_year.py", clr_ro_dir])
subprocess.check_call(["./2_clrro_cleanup.py", all_laws_dir, all_laws_clean_dir])
subprocess.check_call(["./3_clrro_fetch_individual_laws.py", all_laws_clean_dir])
