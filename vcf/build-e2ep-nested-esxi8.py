# Description: Builds Nested ESXi 8 Host using Terraform
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
from os.path import exists
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

'''
Steps:

03. Download main.tf to node controller using paramiko_download_file_to_remote_photon_vm()
04. Create TF variables file
05. Move TF variables file to node controller using paramiko_move_file_to_remote_photon_vm()
06. With Paramiko run docker terraform container with appropriate TF commands
'''

# 03. Download main.tf to node controller 
err = "03. Download main.tf to node controller started."
lib.write_to_logs(err, logfile_name)
err = "    Node Controller IP: "+ip_address
lib.write_to_logs(err, logfile_name)
err = "    main.tf URL: "+config.SCRIPTS().build_nested_esxi8_main_tf_url
lib.write_to_logs(err, logfile_name)
filepath = fullpath+"/"
err = "    Filepath where main.tf is being dropped: "+filepath
lib.write_to_logs(err, logfile_name)
lib.paramiko_download_file_to_remote_photon_vm(ip_address, config.PHOTONOS().username, config.PHOTONOS().password, config.SCRIPTS().build_nested_esxi8_main_tf_url, filepath, config.SCRIPTS().build_nested_esxi8_main_tf_filename)
err = "03. Download main.tf to node controller finished."
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# 03. Create terraform variables file 
err = "03. Create terraform variables file started."
lib.write_to_logs(err, logfile_name)
tf_var_txt = ["# Python generated var file",
"variable \"vsphere_user\" { default = \""+config.E2EP_ENVIRONMENT().esxi_host_username+"\" }",
"variable \"vsphere_pass\" { default = \""+config.UNIVERSAL().password+"\" }",
"variable \"vsphere_serer\" { default = \""+config.E2EP_ENVIRONMENT().esxi_host_ip+"\" }",
"variable \"datacenter_name\" { default = \"ha-datacenter\" }",
"variable \"datastore_name\" { default = \""+config.E2EP_ENVIRONMENT().esxi_host_datastore+"\" }",
"variable \"network_name\" { default = \""+config.E2EP_ENVIRONMENT().esxi_host_virtual_switch+"\" }",
"variable \"esxi_host_name\" { default = \""+config.E2EP_ENVIRONMENT().esxi_host_hostname+"\" }",
"variable \"vm_name\" { default = \""+sys.argv[1]+"\" }",
"variable \"cpu\" { default = 4 }",
"variable \"memory\" { default = 16384 }",
"variable \"guest\" { default = \"other3xLinux64Guest\" }",
"variable \"hostname\" { default = \""+config.NESTED_ESXI8().domain_hostname[0]+"\" }",
"variable \"ip_address\" { default = \""+config.NESTED_ESXI8().ip[0]+"\" }",
"variable \"netmask\" { default = \""+config.E2EP_ENVIRONMENT().subnet_mask+"\" }",
"variable \"default_gateway\" { default = \""+config.E2EP_ENVIRONMENT().default_gw+"\" }",
"variable \"dns\" { default = \""+config.DNS().ip+"\" }",
"variable \"domain\" { default = \""+config.DNS().zone+"\" }",
"variable \"ntp\" { default = \""+config.E2EP_ENVIRONMENT().ntp_server+"\" }",
"variable \"guest_password\" { default = \""+config.E2EP_ENVIRONMENT().ntp_server+"\" }"
]

var_file_name = "var.tf"
var_file_exists = exists(var_file_name)
if var_file_exists:
    err = "    removing old var file"
    lib.write_to_logs(err, logfile_name)
    os.remove(var_file_name)

for line in tf_var_txt:
    lib.append_text_to_file(line+"\n", var_file_name)

err = "03. Create terraform variables file finished."
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)
