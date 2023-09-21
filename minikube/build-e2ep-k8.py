# Description: Installs Minikube (kubernetes) on a Photon controller
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
logfile_name = config.LOGS().minikube
pattern_name = config.MINIKUBE().pattern
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
vm_name = config.MINIKUBE().photon_controller_vm_name
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

# Convert Minikube Install Script to variable
minikube_install_script = os.getcwd()+"/install-minikube.sh"
err = "Pulling scripts from "+minikube_install_script
lib.write_to_logs(err, logfile_name)
minikube_install_raw = lib.populate_var_from_file(minikube_install_script)
minikube_install_commands = minikube_install_raw.split('\n')
err = ""
lib.write_to_logs(err, logfile_name)
err = "Validating commands:"
lib.write_to_logs(err, logfile_name)
i=0
for command in minikube_install_commands:
    err = "    ["+str(i)+"] "+command
    lib.write_to_logs(err, logfile_name)
    i=i+1
err = ""
lib.write_to_logs(err, logfile_name)

# Install Minikube:
err = "Installing Minikube"
lib.write_to_logs(err, logfile_name)
i=0
for command in minikube_install_commands:
    err = "    ["+str(i)+"] "+command
    lib.write_to_logs(err, logfile_name)
    lib.send_command_over_ssh(command, ip_address, E2EP_ENVIRONMENT().photonos_username, E2EP_ENVIRONMENT().photonos_password)
    i=i+1
err = ""
lib.write_to_logs(err, logfile_name)
err = "Finished."
lib.write_to_logs(err, logfile_name)
