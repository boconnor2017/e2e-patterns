# Description: Adds Physical ESXi host to vCenter using Config file
# Author: Brendan O'Connor
# Date: January 2024
# Version: 1.0

# lib and config filenames for the year 
# Must be available in /e2e-patterns repository
lib_filename = "lib2024.py"
config_filename = "config2024.py"

# Base imports
import os
import shutil
import json

# Copy latest lib and config files
fullpath = os.getcwd()
dirs = fullpath.split('/')
count_dirs = len(dirs)
currdir = dirs[count_dirs-1]
homedir = dirs[count_dirs-2]
shell_dir = ""
i=0 
for x in dirs:
    if i == 0:
        shell_dir = "/"
        i=i+1
    if i == (count_dirs-1):
        shell_dir = shell_dir
    if i == (count_dirs-2):
        shell_dir = shell_dir
    else:
        shell_dir = shell_dir+dirs[i]+"/"
        i=i+1

lib_path = shell_dir+homedir+"/"+lib_filename
config_path = shell_dir+homedir+"/"+config_filename
shutil.copy(lib_path, fullpath)
os.rename(lib_filename, "lib.py")
shutil.copy(config_path, fullpath)
os.rename(config_filename, "config.py")

# Import pattern config and library
import config
import lib

# Start log file
logfile_name = config.LOGS().template
pattern_name = config.TEMPLATE().pattern
lib.e2e_patterns_header(logfile_name, pattern_name)
err = ""
lib.write_to_logs(err, logfile_name)

# 01. Add Physical ESXi to vCenter
err = "01. Add Physical ESXi to vCenter:"
lib.write_to_logs(err, logfile_name)
err = "    esxi host: "+config.E2EP_ENVIRONMENT().esxi_host_ip
lib.write_to_logs(err, logfile_name)
session_id = lib.vapi_get_vc_session_id(config.VCSA().fqdn, config.VCSA().username, config.UNIVERSAL().password)
err = "    session id: "+session_id
lib.write_to_logs(err, logfile_name)
folders = lib.vapi_get_vcenter_folders(session_id, config.VCSA().fqdn)
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
