# Description: Deploy a Nested ESXi 8 Appliance
# Author: Brendan O'Connor
# Date: January 2024
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
err = "Building Nested ESXi 8 using OVA:"
lib.write_to_logs(err, logfile_name)
err = "    VM Name: "+sys.argv[1]
lib.write_to_logs(err, logfile_name)
err = "    OVA Source: "+config.ESXI().nested_esxi8_ova_source
lib.write_to_logs(err, logfile_name)
lib.build_nested_esxi8_with_ovftool_container(sys.argv[1], config.ESXI().nested_esxi8_ova_source)
