# Description: Changes default photonos password using PowerCLI container
# Author: Brendan O'Connor
# Date: January 2024
# Version: 3.0

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
logfile_name = config.LOGS().photonos
pattern_name = config.PHOTONOS().pattern
lib.e2e_patterns_header(logfile_name, pattern_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Change IP Address of VM
'''
[1] = vmname
[2] = new password
'''
lib.docker_powercli_change_default_photonos_password(sys.argv[1], sys.argv[2])
