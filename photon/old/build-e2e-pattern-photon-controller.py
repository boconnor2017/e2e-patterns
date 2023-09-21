# Builds a photon controller (a prepped photon appliance ready for building patterns)
# 	Deploy photon: uses ovftool container
#	Change password: uses powercli container
#	Get IP address (DHCP assigned): uses powercli container
#	Configure photon: uses paramiko to ssh into the os 
# Author: Brendan O'Connor
# Date: September 2023 (Version 2.0)

import os
import shutil
import paramiko
import docker
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
err = ""
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)
err = "* * * * * * * * * * * * * * * * * * * * * * * * * * * * *"
lib.write_to_logs(err, logfile_name)
err = "* * * * * * * * * * * * * * * * * * * * * * * * * * * * *"
lib.write_to_logs(err, logfile_name)
err = "Starting build-e2e-pattern-photon-controller.py"
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Build photon controller
lib.build_photon_controller(sys.argv[1], sys.argv[2], logfile_name)
