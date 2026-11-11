#!/usr/bin/env python3
"""Run every experiment on this branch:  python3 -I experiments/run_all.py"""
import os
import subprocess
import sys

here = os.path.dirname(os.path.abspath(__file__))
names = ["exp_cap_centres.py", "exp_cap_centre_general.py",
         "exp_shell_exact.py", "exp_model_c.py", "exp_model_d.py",
         "exp_production_readonly.py",
         "exp_review_i2_independent.py", "exp_i3_extended_verification.py",
         "exp_i3_encoder_audit.py", "exp_i3_radix5_generators.py", "exp_i3_model_h5.py"]
bad = 0
for n in names:
    r = subprocess.run([sys.executable, "-I", "-B", os.path.join(here, n)])
    bad += r.returncode != 0
print("ALL PASSED" if not bad else f"{bad} FAILED")
sys.exit(1 if bad else 0)
