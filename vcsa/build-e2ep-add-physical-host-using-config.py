# Description: Adds Physical ESXi host to vCenter using Config file
# Author: Brendan O'Connor
# Date: January 2024
# Version: 1.0

# Base imports
import os
import shutil
import sys
import json

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
logfile_name = config.LOGS().vcsa
pattern_name = config.ESXI().pattern
lib.e2e_patterns_header(logfile_name, pattern_name)
err = ""
lib.write_to_logs(err, logfile_name)

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

# Get Photon Controller IP
vm_name = config.VCSA().photon_controller_vm_name
err = "Getting IP address of photon controller:"
lib.write_to_logs(err, logfile_name)
err = "    vm name: "+vm_name
lib.write_to_logs(err, logfile_name)
ip_address = lib.get_vm_ip_address(vm_name)
err = "    ip address: "+ip_address
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Check for input parameters
err = "Checking for input parameters:"
lib.write_to_logs(err, logfile_name)
err = "    parameters: "+sys.argv[1]
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Add ESXi to vCenter
err = "Adding host to vCenter:"
lib.write_to_logs(err, logfile_name)
err = "    esxi host: "+sys.argv[1]
lib.write_to_logs(err, logfile_name)
session_id = lib.get_vc_session_id(config.VCSA().fqdn, config.VCSA().username, config.UNIVERSAL().password)
err = "    session id: "+session_id
lib.write_to_logs(err, logfile_name)
folders = lib.get_vcenter_folders(session_id, config.VCSA().fqdn)
folders_json_dump = json.dumps(folders)
folders_json_load = json.loads(folders_json_dump)

err = "    folders: "+session_id
lib.write_to_logs(err, logfile_name)
i=0
for folder in folders_json_load:
    err = "        ["+str(i)+"]"
    lib.write_to_logs(err, logfile_name)
    err = "        folder: "+folder["folder"]
    lib.write_to_logs(err, logfile_name)
    err = "        name: "+folder["name"]
    lib.write_to_logs(err, logfile_name)
    err = "        type: "+folder["type"]
    err = ""
    lib.write_to_logs(err, logfile_name)
    i=i+1

vc_folder = folders_json_load[1]["folder"]
result = lib.add_host_to_vcenter(session_id, config.VCSA().fqdn, config.E2EP_ENVIRONMENT().esxi_host_ip, config.UNIVERSAL().password, config.ESXI().username, vc_folder)
