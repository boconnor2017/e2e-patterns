# Description: Builds and Configures an NSX Manager using a Photon controller
# Author: Brendan O'Connor
# Date: September 2023
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
logfile_name = config.LOGS().nsx
pattern_name = config.TEMPLATE().pattern
lib.e2e_patterns_header(logfile_name, pattern_name)
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
vm_name = config.TEMPLATE().photon_controller_vm_name
if skip_build_photon_controller:
    skip_build_photon_controller = True 
else:
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

# Downloading local.py to Photon Controller
err = "Downloading local.py to photon controller."
lib.write_to_logs(err, logfile_name)
url = "https://raw.githubusercontent.com/boconnor2017/e2e-patterns/main/terraform/install-nsx-manager/local.py"
local_file = "/usr/local/drop/local.py"
err = lib.download_file_to_photon_controller(ip_address, config.E2EP_ENVIRONMENT().photonos_username, config.E2EP_ENVIRONMENT().photonos_password, url, local_file)
lib.write_to_logs(err, logfile_name)

# Run local.py on Photon Controller
err = "Running local.py on photon controller."
lib.write_to_logs(err, logfile_name)
cmd = "python3 /usr/local/drop/local.py"
err = "    cmd: "+cmd 
lib.write_to_logs(err, logfile_name)
err = lib.send_command_over_ssh(cmd, ip, un, pw)
lib.write_to_logs(err, logfile_name)
