# Description: Template for building terraform variables using config.py
# Author: Brendan O'Connor
# Date: January 2024
# Version: 1.0

# Base imports
import os
from os.path import exists
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
logfile_name = config.LOGS().template
pattern_name = config.TEMPLATE().pattern
lib.e2e_patterns_header(logfile_name, pattern_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Build Terraform Variables file 
err = "Building terraform variables file"
lib.write_to_logs(err, logfile_name)
tf_var_txt = ["# Python generated var file",
"variable \"vsphere_user\" { default = \""+config.E2EP_ENVIRONMENT().esxi_host_username+"\" }",
"variable \"vsphere_pass\" { default = \""+config.UNIVERSAL().password+"\" }",
"variable \"vsphere_serer\" { default = \""+config.E2EP_ENVIRONMENT().esxi_host_ip+"\" }",
"variable \"datacenter_name\" { default = \"ha-datacenter\" }",
"variable \"datastore_name\" { default = \""+config.E2EP_ENVIRONMENT().esxi_host_datastore+"\" }",
"variable \"network_name\" { default = \""+config.E2EP_ENVIRONMENT().esxi_host_virtual_switch+"\" }",
"variable \"esxi_host_name\" { default = \"esxi1\" }",
"variable \"vm_name\" { default = \"tf-test-02\" }",
"variable \"cpu\" { default = 1 }",
"variable \"memory\" { default = 1024 }",
"variable \"guest\" { default = \"other3xLinux64Guest\" }"]

var_file_name = "var.tf"
var_file_exists = exists(var_file_name)
if var_file_exists:
    err = "    removing old var file"
    lib.write_to_logs(err, logfile_name)
    os.remove(var_file_name)

for line in tf_var_txt:
    lib.append_text_to_file(line+"\n", var_file_name)
