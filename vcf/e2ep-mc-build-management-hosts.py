# Description: Builds Nested ESXi Management Cluster for VCF 5.1 Call from MC to NC
# Author: Brendan O'Connor
# Date: February 2024
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

# 01. Check for node controller
err = "01. Check for node controller started."
lib.write_to_logs(err, logfile_name)
node_controller_exists = lib.e2e_check_for_node_controller(config.NESTED_ESXI8().photon_controller_vm_name)
if node_controller_exists == 1:
    err = "    "+config.NESTED_ESXI8().photon_controller_vm_name+" exists."
    lib.write_to_logs(err, logfile_name)
else:
    err = "    "+config.NESTED_ESXI8().photon_controller_vm_name+" does not exist."
    lib.write_to_logs(err, logfile_name)
    err = "    Running e2e_build_node_controller()."
    lib.write_to_logs(err, logfile_name)
    lib.e2e_build_node_controller(config.NESTED_ESXI8().photon_controller_vm_name, logfile_name)
err = "01. Check for node controller finished."
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# 02. Get IP Address of the node controller 
err = "02. Get IP Address of the node controller started."
lib.write_to_logs(err, logfile_name)
ip_address = lib.docker_powercli_get_vm_ip_address(config.NESTED_ESXI8().photon_controller_vm_name)
err = "    IP Address of "+config.NESTED_ESXI8().photon_controller_vm_name+" is "+ip_address
lib.write_to_logs(err, logfile_name)
err = "02. Get IP Address of the node controller finished."
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# 03. Prompt User to Upload Nested ESXi 8 ova
if node_controller_exists == 0:
    err = "03. Prompt User to Upload Nested ESXi 8 ova started."
    lib.write_to_logs(err, logfile_name)
    err = "    Prompting user to upload "+config.NESTED_ESXI8().nested_esxi8_ova_filename+" to "+ip_address
    lib.write_to_logs(err, logfile_name)
    print("")
    print("")
    print("--------------------------------------------------------------")
    print("The script is paused. User input is required.")
    print("Please upload "+config.NESTED_ESXI8().nested_esxi8_ova_filename+" to "+ip_address+" /usr/local/drop repository.")
    print("The cloud builder ova is a large file, it is recommended you change the disk size of the node controller to 50GB.")
    print("")
    print("")
    userprompt = input("Hit ENTER key when finished.")
    print("")
    print("")
    print("--------------------------------------------------------------")
    err = "    User prompt: "+userprompt
    lib.write_to_logs(err, logfile_name)    
    err = "03. Prompt User to Upload Nested ESXi 8 ova finished."
    lib.write_to_logs(err, logfile_name)
    err = ""
    lib.write_to_logs(err, logfile_name)
else:
    err = "03. Skipping step 3. Prompt not needed."
    lib.write_to_logs(err, logfile_name)
    err = ""
    lib.write_to_logs(err, logfile_name)


# 04. Call python wrapper on node controller
err = "04. Call python wrapper on node controller."
lib.write_to_logs(err, logfile_name)
err = "    04A. Node Controller IP Address: "+ip_address
lib.write_to_logs(err, logfile_name)
err = "    04B. Path to Python wrapper: "+fullpath+"/"
lib.write_to_logs(err, logfile_name)
err = "    04C. Python wrapper: "+sys.argv[1]
lib.write_to_logs(err, logfile_name)
lib.e2e_run_python_wrapper_on_node_from_master(ip_address, config.PHOTONOS().username, config.PHOTONOS().password, fullpath+"/", sys.argv[1])
err = "04. Master Controller job is finished."
lib.write_to_logs(err, logfile_name)
