# Description: Installs Minikube (kubernetes) on a Photon controller
# Author: Brendan O'Connor
# Date: August 2023
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
logfile_name = config.LOGS().minikube
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
err = "Starting build-e2e-pattern-minikube.py"
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
src_file = '/usr/local/e2e-patterns/photon/change-photon_default_pw.ps1'
des_dir = os.getcwd()
err = "    copying "+src_file+" and copying to "+des_dir
outpt = shutil.copy(src_file, des_dir)
err = ""
lib.write_to_logs(err, logfile_name)

# Build photon controller
lib.build_photon_controller(sys.argv[1], sys.argv[2], logfile_name)
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
