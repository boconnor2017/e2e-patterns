# Description: Aria Lifecycle Manager using Easy Installer ISO mounted to a Photon controller
# Author: Brendan O'Connor
# Date: October 2023
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
logfile_name = config.LOGS().aria
pattern_name = config.ARIA_LCM().pattern
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
vm_name = config.ARIA_LCM().photon_controller_vm_name
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

# Create directory /usr/local/mount
err = "Creating mount directory."
lib.write_to_logs(err, logfile_name)
create_dir_cmd = "mkdir /usr/local/mount"
err = "    command: "+create_dir_cmd
lib.write_to_logs(err, logfile_name)
lib.send_command_over_ssh(create_dir_cmd, photon_controller_ip_address, config.E2EP_ENVIRONMENT().photonos_username, config.E2EP_ENVIRONMENT().photonos_password)
err = ""
lib.write_to_logs(err, logfile_name)

# Prompt user to continue with script
if skip_build_photon_controller:
    skip_build_photon_controller = True 
else:
    err = "Prompting user and pausing until the ISO is attached to the photon controller..."
    lib.write_to_logs(err, logfile_name)
    print("")
    print("")
    print("This next step requires manual intervention.")
    print("Attach the Aria LCM Easy Installer ISO to the photon controller (vm name: "+config.ARIA_LCM().photon_controller_vm_name+")")
    pressanykeytocontinue = input("Press Enter to continue:")
    print("")
    print("")
    err = "Prompt received. Continuing with the script. "
    lib.write_to_logs(err, logfile_name)
    err = ""
    lib.write_to_logs(err, logfile_name)

# Mount ISO to the photon controller 
err = "Mounting ISO:"
lib.write_to_logs(err, logfile_name)
mount_iso_cmd = "mount -t iso9660 -o loop /dev/cdrom /usr/local/mount/"
err = "    command: "+mount_iso_cmd
lib.write_to_logs(err, logfile_name)
lib.send_command_over_ssh(mount_iso_cmd, photon_controller_ip_address, config.E2EP_ENVIRONMENT().photonos_username, config.E2EP_ENVIRONMENT().photonos_password)
err = ""
lib.write_to_logs(err, logfile_name)
