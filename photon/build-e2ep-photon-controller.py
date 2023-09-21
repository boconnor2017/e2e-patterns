# Description: Builds a Photon Controller from the Master Controller
# Author: Brendan O'Connor
# Date: September 2023
# Version: 2.0

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
pattern_name = "A-04: Deploy a Photon controller"
lib.e2e_patterns_header(logfile_name, pattern_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Photon controller prerequisites
err = "Copying PowerCLI scripts from /photon repo"
lib.write_to_logs(err, logfile_name)
src_file = src_dir+'/photon/change-photon_default_pw.ps1'
outpt = shutil.copy(src_file, des_dir)
src_file = src_dir+'/photon/get-vm-ip.ps1'
outpt = shutil.copy(src_file, des_dir)
src_file = src_dir+'/photon/change-vm-ip.ps1'
outpt = shutil.copy(src_file, des_dir)
err = ""
lib.write_to_logs(err, logfile_name)

# Build photon controller 
vm_name = sys.argv[1]
err = "Building photon controller."
lib.write_to_logs(err, logfile_name)
lib.build_photon_controller(vm_name, config.E2EP_ENVIRONMENT().photonos_source, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Get Photon Controller IP
err = "Getting IP address of photon controller:"
lib.write_to_logs(err, logfile_name)
err = "    vm name: "+vm_name
lib.write_to_logs(err, logfile_name)
ip_address = lib.get_vm_ip_address(vm_name)
err = "    ip address: "+ip_address
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)
