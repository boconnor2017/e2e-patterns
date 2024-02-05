# Description: Builds CloudBuilder for VCF 5.1 (run from NC)
# Author: Brendan O'Connor
# Date: February 2024
# Version: 2.1

# lib and config filenames for the year 
# Must be available in /e2e-patterns repository
lib_filename = "lib2024.py"
config_filename = "config2024.py"

# Base imports
import os
import shutil

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
pattern_name = config.CLOUD_BUILDER().pattern
lib.e2e_patterns_header(logfile_name, pattern_name)
err = ""
lib.write_to_logs(err, logfile_name)

# 01. Build Cloud Builder
err = "01. Build Cloud Builder started."
lib.write_to_logs(err, logfile_name)
err = "    01A. VM Name: "+config.CLOUD_BUILDER().cb_vm_name
lib.write_to_logs(err, logfile_name)
logfile_name = fullpath+"/"+logfile_name
err = "    01B. Specifying proper logfile directory: "+logfile_name
lib.write_to_logs(err, logfile_name)
lib.docker_powercli_create_cloud_builder(config.CLOUD_BUILDER().cb_vm_name)
err = "01. Build Cloud Builder finished."
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)
