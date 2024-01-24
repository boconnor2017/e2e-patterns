# Description: Deploy a Nested ESXi Appliance
# Author: Brendan O'Connor
# Date: November 2023
# Version: 1.0

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
logfile_name = config.LOGS().esxi 
pattern_name = config.ESXI().pattern
lib.e2e_patterns_header(logfile_name, pattern_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Deploy Nested ESXi 
lib.build_photon_with_ovftool_container(sys.argv[1], config.ESXI().nested_esxi_ova_source) #reusing this script for a non photon build 
