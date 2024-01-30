# Description: Builds a nested ESXi host using PowerCLI (Custom)
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
import sys

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
logfile_name = config.LOGS().vcf
pattern_name = config.NESTED_ESXI8().pattern
lib.e2e_patterns_header(logfile_name, pattern_name)
err = ""
lib.write_to_logs(err, logfile_name)

'''
[1] VM Name
[2] Number of CPUs
[3] Memory (MB)
[4] Hostname
[5] IP Address
[6] Netmask 
[7] Gateway
[8] DNS (comma separated NO SPACES)
[9] Domain
[10] NTP
[11] Password
'''
err = "Building nested ESXi host:"
lib.write_to_logs(err, logfile_name)
err = "    VM Name:"+sys.argv[1]
lib.write_to_logs(err, logfile_name)
err = "    CPU:"+sys.argv[2]
lib.write_to_logs(err, logfile_name)
err = "    Memory (MB):"+sys.argv[3]
lib.write_to_logs(err, logfile_name)
lib.docker_powercli_create_nested_esxi8_dhcp(sys.argv[1], sys.argv[2], sys.argv[3])
lib.docker_powercli_create_nested_esxi8_custom(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11])
