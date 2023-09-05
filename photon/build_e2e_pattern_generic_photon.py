# Builds PhotonOS virtual appliance using ovftool container
# Author: Brendan O'Connor
# Date: August 2023
# Add python script (example below)
import os
import shutil
import subprocess
import sys

# Get pattern config file
src_file = '/usr/local/e2e-patterns/config.py'
des_dir = os.getcwd()
print("Retrieving config file from "+src_file+" and copying to "+des_dir)
outpt = shutil.copy(src_file, des_dir)
print(str(outpt))
print("")

# Get pattern library
src_file = '/usr/local/e2e-patterns/lib.py'
des_dir = os.getcwd()
print("Retrieving library file from "+src_file+" and copying to "+des_dir)
outpt = shutil.copy(src_file, des_dir)
print(str(outpt))
print("")

import config
import lib

# Start log file
logfile_name = config.LOGS().photonos
err = "Starting wrapper-build-e2e-pattern-photon.py"
lib.write_to_logs(err, logfile_name)
err = "Input variables:"
lib.write_to_logs(err, logfile_name)
i=0 
for args in sys.argv:
	err = "    "+args[i]
	lib.write_to_logs(err, logfile_name)
	i=i+1

# Virtual Machine Details
class VM():
	name = sys.argv[1] # as displayed in vCenter
	source = sys.argv[2] # (syntax: ova-name.ova)

err = "Class VM():"
lib.write_to_logs(err, logfile_name)
err = "	   name: "+VM().name
lib.write_to_logs(err, logfile_name)
err = "	   source: "+VM().source
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Build OVF
err = "Building Generic Photon using ovftool container."
lib.write_to_logs(err, logfile_name)
err = lib.build_photon_with_ovftool_container(VM().name, VM().source)
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)


