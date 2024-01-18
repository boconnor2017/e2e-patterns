# Description: Creates DNS Zone on the Tanium Server using config parameters
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
logfile_name = config.LOGS().dns
pattern_name = config.DNS().pattern
lib.e2e_patterns_header(logfile_name, pattern_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Get Tanium Token using credentials
err = "Getting Tanium Token using credentials:"
lib.write_to_logs(err, logfile_name)
tanium_token = lib.tanium_get_token('admin', config.UNIVERSAL().password)
err = "    Tanium Token: "+tanium_token
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Create DNS Zone
err = "Creating DNS Zone."
lib.write_to_logs(err, logfile_name)
api_response = lib.tanium_create_dns_zone(tanium_token, config.DNS().zone)
err = "    API Response: "+str(api_response)
lib.write_to_logs(err, logfile_name)
