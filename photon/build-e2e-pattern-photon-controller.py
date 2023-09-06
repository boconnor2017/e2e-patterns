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

# Virtual Machine Details
class VM():
	name = sys.argv[1] # as displayed in vCenter
	source = sys.argv[2] # (syntax: ova-name.ova)
	prep_script = "/usr/local/prep-photon.sh"
	refresh_script = "/usr/local/refresh-e2e-patterns.sh"

err = "VM() Class:"
lib.write_to_logs(err, logfile_name)
err = "    .name: "+VM().name
lib.write_to_logs(err, logfile_name)
err = "    .source: "+VM().source
lib.write_to_logs(err, logfile_name)
err = "    .prep_scrip: "+VM().prep_script
lib.write_to_logs(err, logfile_name)
err = "    .refresh_script: "+VM().refresh_script
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Deploy Photon Appliance using ovftool container
err = "Building generic photon appliance:"
lib.write_to_logs(err, logfile_name)
err = lib.build_photon_with_ovftool_container(VM().name, VM().source)
lib.write_to_logs(err, logfile_name)
err = ""

# Pause to allow ova to complete its build 
seconds = (60*2)
err = "Pausing for "+str(seconds)+" seconds to let the ova to complete its build..."
lib.write_to_logs(err, logfile_name)
lib.pause_python_for_duration(seconds)
err = "Resuming script."
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Change default password of the Photon Appliance
err = "Changing the default password using powercli container."
lib.write_to_logs(err, logfile_name)
lib.change_vm_os_password(VM().name, config.E2EP_ENVIRONMENT().photonos_password)

# Pause to allow password change to take effect 
seconds = (20)
err = "Pausing for "+str(seconds)+" seconds to let the password change to take effect..."
lib.write_to_logs(err, logfile_name)
lib.pause_python_for_duration(seconds)
err = "Resuming script."
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Get IP Address of the photon vm
err = "Getting ip address:"
lib.write_to_logs(err, logfile_name)
photon_ip_address = lib.get_vm_ip_address(VM().name)
err = "    IP Address: "+photon_ip_address
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Test SSH Connection to photon
err = "Testing SSH connection to "+photon_ip_address
lib.write_to_logs(err, logfile_name)
ssh_test = lib.connect_to_ssh_server_test(photon_ip_address, config.E2EP_ENVIRONMENT().photonos_username, config.E2EP_ENVIRONMENT().photonos_password)
if ssh_test:
	err = "   connection succeeded."
	lib.write_to_logs(err, logfile_name)
else:
	err = "[!] connection failed"
	lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Download prep-photon scripts
if ssh_test:
    err = "Downloading photon prep scripts."
    lib.write_to_logs(err, logfile_name)
    lib.download_photon_prep_script_via_ssh(photon_ip_address, config.E2EP_ENVIRONMENT().photonos_username, config.E2EP_ENVIRONMENT().photonos_password)
    err = ""
    lib.write_to_logs(err, logfile_name)

# Validate prep-photon script
if ssh_test:
    err = "Pulling prep script into variable"
    lib.write_to_logs(err, logfile_name)
    prep_photon_script_source = "/usr/local/prep-photon.sh"
    prep_photon_script_txt = lib.populate_var_from_file(prep_photon_script_source)
    prep_photon_script_commands = prep_photon_script_txt.split('\n')
    err = "Validating Commands:"
    lib.write_to_logs(err, logfile_name)
    i=0
    for commands in prep_photon_script_commands:
        err = "    ["+str(i)+"] "+commands
        lib.write_to_logs(err, logfile_name)
        i=i+1

err = ""
lib.write_to_logs(err, logfile_name)

# Run prep-photon script
if ssh_test:
    err = "Pulling prep script into variable"
    lib.write_to_logs(err, logfile_name)
    prep_photon_script_source = "/usr/local/prep-photon.sh"
    prep_photon_script_txt = lib.populate_var_from_file(prep_photon_script_source)
    prep_photon_script_commands = prep_photon_script_txt.split('\n')
    err = "Running Commands:"
    lib.write_to_logs(err, logfile_name)
    i=0
    for commands in prep_photon_script_commands:
        err = "    Running: ["+str(i)+"] "+commands
        lib.write_to_logs(err, logfile_name)
        stdout = lib.send_command_over_ssh(commands, photon_ip_address, config.E2EP_ENVIRONMENT().photonos_username, config.E2EP_ENVIRONMENT().photonos_password)
        i=i+1

err = "Finished."
lib.write_to_logs(err, logfile_name)
