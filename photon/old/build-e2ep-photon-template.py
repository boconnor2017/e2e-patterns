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
err = lib.create_vm_with_powercli(config.PHOTONOS().template_name)
err = str(err)
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Prompt user to attach ISO
err = "Prompting user to attach ISO"
lib.write_to_logs(err, logfile_name)
print("The script is paused. Manual configuration is required to continue.")
print("    Step 1: Click \"Edit Settings\" for virtual machine "+config.PHOTONOS().template_name)
print("    Step 2: Change \"Memory\" to 2048 MB")
print("    Step 3: Change \"Hard Disk\" to 16 GB")
print("    Step 4: Click \"Add other device\"")
print("    Step 5: Add a \"CD/DVD drive\"")
print("    Step 6: Select \"Datastore ISO file\" from the CD/DVD Drive and select the PhotonOS ISO.")
print("    Step 7: Ensure \"Connect\" checkbox is selected next to the CD/DVD Drive.")
print("    Step 8: Click \"Save\".")
print("")
input("When these steps are completed, press <ENTER>")

# Start VM with PowerCLI 
err = "Starting VM "+config.PHOTONOS().template_name
lib.write_to_logs(err, logfile_name)
err = lib.start_vm_with_powercli(config.PHOTONOS().template_name)
err = str(err)
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)
