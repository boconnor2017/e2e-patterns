# Description: Builds nested management hosts for VCF 5.1
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
# 01. Build 4x Nested ESXi Hosts using config file
err = "01. Build 4x Nested ESXi Hosts using config file started."
lib.write_to_logs(err, logfile_name)
logfile_name = fullpath+"/"+logfile_name
err = "    01A. Specify proper logfile to account for directory change: "+logfile_name
lib.write_to_logs(err, logfile_name)
i=0 
for x in config.NESTED_ESXI8().esxi_vm_name:
    err = "    ------------------------------"
    lib.write_to_logs(err, logfile_name)
    err = "    ["+str(i)+"]: "+config.NESTED_ESXI8().esxi_vm_name[i]
    lib.write_to_logs(err, logfile_name)
    err = "        CPUs: "+config.NESTED_ESXI8().numcpu
    lib.write_to_logs(err, logfile_name)
    err = "        Memory (MB): "+config.NESTED_ESXI8().mem_mb
    lib.write_to_logs(err, logfile_name)
    err = "        hostname: "+config.NESTED_ESXI8().domain_hostname[i]
    lib.write_to_logs(err, logfile_name)
    err = "        IP Address: "+config.NESTED_ESXI8().ip[i]
    lib.write_to_logs(err, logfile_name)
    err = "        Netmask: "+config.E2EP_ENVIRONMENT().subnet_mask
    lib.write_to_logs(err, logfile_name)
    err = "        Gateway: "+config.E2EP_ENVIRONMENT().default_gw
    lib.write_to_logs(err, logfile_name)
    err = "        DNS: "+config.DNS().ip+",8.8.8.8"
    lib.write_to_logs(err, logfile_name)
    err = "        Domain: "+config.DNS().zone
    lib.write_to_logs(err, logfile_name)
    err = "        NTP: "+config.E2EP_ENVIRONMENT().ntp_server
    lib.write_to_logs(err, logfile_name)
    lib.docker_powercli_create_nested_esxi8_custom(config.NESTED_ESXI8().esxi_vm_name[i], config.NESTED_ESXI8().numcpu, config.NESTED_ESXI8().mem_mb, config.NESTED_ESXI8().domain_hostname[i], config.NESTED_ESXI8().ip[i], config.E2EP_ENVIRONMENT().subnet_mask, config.E2EP_ENVIRONMENT().default_gw, config.DNS().ip+",8.8.8.8", config.DNS().zone, config.E2EP_ENVIRONMENT().ntp_server, config.UNIVERSAL().password)
    i=i+1

err = ""
lib.write_to_logs(err, logfile_name)
err = "Management domain finished."
lib.write_to_logs(err, logfile_name)
