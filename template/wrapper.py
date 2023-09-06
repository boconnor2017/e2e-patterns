# Python template for E2E Patterns
# Python files should follow this naming convention: build-e2e-pattern-<NAME>.py
# Copy Template Below
# # # # # # # # # # # # # # # # # #
# Description: <Add description>
# Author: Brendan O'Connor
# Date: <month year>
# Version: <version>

# Base imports
import os
import shutil
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

# Import pattern config and library
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

# CUSTOM:
