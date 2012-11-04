#!/usr/bin/env python
import os
import subprocess
import platform

work_dir = "/tmp/legilibere/"

if not os.path.exists(work_dir):
    os.makedirs(work_dir)
    print('The work directory did not exist so I created it')
    print(work_dir)

clr_ro_dir = os.path.join(work_dir, 'clr_ro');
subprocess.check_call(["./1_clrro_fetch_laws_per_year.py", clr_ro_dir])
subprocess.check_call(["./2_clrro_cleanup.py.py", clr_ro_dir])
subprocess.check_call(["./3_clrro_fetch_individual_laws.py", clr_ro_dir])
