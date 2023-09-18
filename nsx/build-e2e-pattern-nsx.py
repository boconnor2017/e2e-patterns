# Description: Installs NSX using a Photon controller
# Author: Brendan O'Connor
# Date: September 2023
# Version: 1.0

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
logfile_name = config.LOGS().nsx
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
err = "Starting build-e2e-pattern-nsx.py"
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Photon controller prerequisites
err = "Photon controller prerequisites:"
lib.write_to_logs(err, logfile_name)
src_file = '/usr/local/e2e-patterns/photon/change-photon_default_pw.ps1'
des_dir = os.getcwd()
err = "    copying "+src_file+" and copying to "+des_dir
outpt = shutil.copy(src_file, des_dir)
src_file = '/usr/local/e2e-patterns/photon/get-vm-ip.ps1'
des_dir = os.getcwd()
err = "    copying "+src_file+" and copying to "+des_dir
outpt = shutil.copy(src_file, des_dir)
src_file = '/usr/local/e2e-patterns/photon/change-vm-ip.ps1'
des_dir = os.getcwd()
err = "    copying "+src_file+" and copying to "+des_dir
outpt = shutil.copy(src_file, des_dir)
err = ""
lib.write_to_logs(err, logfile_name)

# Check for input parameters
err = "Checking for input parameters:"
lib.write_to_logs(err, logfile_name)
err = "    parameters: "+sys.argv[1]
lib.write_to_logs(err, logfile_name)
if sys.argv[1] == "-p":
    skip_build_photon_controller = True
    err = "    skipping build photon controller"
    lib.write_to_logs(err, logfile_name)
else:
    skip_build_photon_controller = False

# Build photon controller
if skip_build_photon_controller:
    skip_build_photon_controller = True 
else:
    err = "Building photon controller:"
    lib.write_to_logs(err, logfile_name)
    lib.build_photon_controller(config.NSX().photon_controller_vm_name, config.NSX().photon_source, logfile_name)
    err = ""
    lib.write_to_logs(err, logfile_name)

# Get VM IP
err = "Getting IP address of photon controller:"
lib.write_to_logs(err, logfile_name)
ip_address = lib.get_vm_ip_address(sys.argv[1])
err = "    ip address: "+ip_address
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

'''
Install NSX:
01. Build photon controller 
02. Download OVFTool OVA to the /usr/local/drio repo of the photon controller
03. Download NSX OVA to the /usr/local/drop repo of the photon controller
04. Using Install NSX using OVFTool
'''

# Prompt user to continue with script
if skip_build_photon_controller:
    skip_build_photon_controller = True 
else:
    err = "Prompting user and pausing until the OVA is downloaded to the photon controller..."
    lib.write_to_logs(err, logfile_name)
    print("")
    print("")
    print("This next step requires manual intervention.")
    print("Download the OVFTool bundle (see Pattern A-01 for details) to the photon controller (vm name: "+config.VCSA().photon_controller_vm_name+")")
    print("AND")
    print("Download the NSX-T OVA to the photon controller (vm name: "+config.VCSA().photon_controller_vm_name+")")
    pressanykeytocontinue = input("Press Enter to continue:")
    print("")
    print("")
    err = "Prompt received. Continuing with the script. "
    lib.write_to_logs(err, logfile_name)
    err = ""
    lib.write_to_logs(err, logfile_name)

#Install NSX using OVFtool container
err = "Installing NSX with OVFTool container"
lib.write_to_logs(err, logfile_name)
err = lib.build_nsx_with_ovftool_container()
lib.write_to_logs(err, logfile_name)
