# Description: local.py for Pattern C-03
# Author: Brendan O'Connor
# Date: October 2023
# Version: 1.0

# Base imports
import os
from os.path import exists
import shutil
import sys

# Get pattern config file and library
os.chdir("/usr/local/drop")
src_file = '/usr/local/e2e-patterns/config.py'
des_dir = '/usr/local/drop'
outpt = shutil.copy(src_file, des_dir)
src_file = '/usr/local/e2e-patterns/lib.py'
des_dir = '/usr/local/drop'
outpt = shutil.copy(src_file, des_dir)

# Import pattern config and library
import config
import lib

# Start log file
logfile_name = config.LOGS().vcf
pattern_name = config.CLOUD_BUILDER().pattern
lib.e2e_patterns_header(logfile_name, pattern_name)
err = ""
lib.write_to_logs(err, logfile_name)

err = "Starting local.py"
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Build cb_vars.tf file
err = "Building cb_vars.tf file"
lib.write_to_logs(err, logfile_name)
tf_var_txt = ["# cb.tfvars file",
"variable \"data_center\" { default = \""+config.VCSA().datacenter+"\" }" ,
"variable \"vds\" { default = \""+config.E2EP_ENVIRONMENT().esxi_host_virtual_switch+"\" }",
"variable \"workload_datastore\" { default = \""+config.E2EP_ENVIRONMENT().esxi_host_datastore+"\" }",
"variable \"compute_host\" {default = \""+config.E2EP_ENVIRONMENT().esxi_host_ip+"\"}",
"variable \"vsphere_server\" {default = \""+config.VCSA().ip+"\"}",
"variable \"vsphere_user\" { default = \""+config.VCSA().username+"\"}",
"variable \"vsphere_password\" { default = \""+config.UNIVERSAL().password+"\"}",
"variable \"mgmt_pg\" { default = \""+config.E2EP_ENVIRONMENT().esxi_host_virtual_switch+"\" }",
"variable \"vm_name\" { default = \""+config.CLOUD_BUILDER().cb_vm_name+"\" }",
"variable \"local_ovf_path\" { default = \"/usr/local/drop/"+config.CLOUD_BUILDER().cb_ova_source+"\" }",
"variable \"FIPS_ENABLE\" { default = \"False\" }",
"variable \"guestinfo_ADMIN_PASSWORD\" { default = \""+config.CLOUD_BUILDER().password+"\" }" ,
"variable \"guestinfo_ADMIN_USERNAME\" { default =  \"admin\" },
"variable \"guestinfo_DNS\"            { default = \""+config.DNS().ip+"\"}",
"variable \"guestinfo_domain\"         { default = \""+config.DNS().zone+"\"}",
"variable \"guestinfo_gateway\"        { default = \""+config.E2EP_ENVIRONMENT().default_gw+"\"}",
"variable \"guestinfo_hostname\"       { default = \""+config.CLOUD_BUILDER().domain_hostname+"\"}",
"variable \"guestinfo_ip0\"            { default = \""+config.CLOUD_BUILDER().ip+"\"}",
"variable \"guestinfo_netmask0\"       { default = \""+config.E2EP_ENVIRONMENT().subnet_mask+"\"}",
"variable \"guestinfo_ntp\"            { default = \""+config.E2EP_ENVIRONMENT().ntp_server+"\"}",
"variable \"guestinfo_ROOT_PASSWORD\"  { default = \""+config.CLOUD_BUILDER().password+"\" }" ,
"variable \"guestinfo_searchpath\"     { default = \""+config.DNS().zone+"\"}",
"variable \"vm_vmname\"                { default = \""+config.CLOUD_BUILDER().domain_hostname+"\"}"
]

tf_var_file_name = "cb_var.tf"
tf_var_file_exists = exists(tf_var_file_name)
if tf_var_file_exists:
    err = "    removing old cb_vars.tf file"
    lib.write_to_logs(err, logfile_name)
    os.remove(tf_var_file_name)

for line in tf_var_txt:
    lib.append_text_to_file(line+"\n", tf_var_file_name)

# Run terraform init 
stdout = lib.run_terraform_init(des_dir)
stdout = stdout.split('\n')

for ln in stdout:
    err = str(ln)
    lib.write_to_logs(err, logfile_name)

# Run terraform apply
stdout = lib.run_terraform_apply(des_dir)
stdout = stdout.split('\n')

for ln in stdout:
    err = str(ln)
    lib.write_to_logs(err, logfile_name)

err = "Finished."
lib.write_to_logs(err, logfile_name)
