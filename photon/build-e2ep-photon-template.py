# Description: Build Photon template from ISO (A-06)
# Author: Brendan O'Connor
# Date: January 2024
# Version: Version 1.0

# Base imports
import os
import shutil
import sys

# Get pattern config file and library
des_dir = str(os.getcwd())
os.chdir("../")
src_dir = str(os.getcwd())
os.chdir(des_dir)
src_file = src_dir+'/config.py'
outpt = shutil.copy(src_file, des_dir)
src_file = src_dir+'/lib.py'
outpt = shutil.copy(src_file, des_dir)

# Import pattern config and library
import config
import lib

# Start log file
logfile_name = config.LOGS().photonos
pattern_name = config.PHOTONOS().pattern
lib.e2e_patterns_header(logfile_name, pattern_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Build Standard VM
err = "Building standard virtual machine."
lib.write_to_logs(err, logfile_name)
lib.create_vm_with_powercli(config.PHOTONOS().template_name)
