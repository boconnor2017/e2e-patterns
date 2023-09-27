# Description: local.py for Pattern C-02
# Author: Brendan O'Connor
# Date: September 2023
# Version: 1.0

# Base imports
import os
from os.path import exists
import shutil
import sys

# Get pattern config file and library
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
logfile_name = config.LOGS().nsx
pattern_name = config.NSX().pattern
lib.e2e_patterns_header(logfile_name, pattern_name)
err = ""
lib.write_to_logs(err, logfile_name)

err = "Starting local.py"
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Build nsx_vars.tf file
err = "Building nsx_vars.tf file"
lib.write_to_logs(err, logfile_name)
tf_var_txt = ["# nsx.tfvars file",
"variable \"data_center\" { default = \""+config.VCSA().datacenter+"\" }" ,
"variable \"vds\" { default = \""+config.E2EP_ENVIRONMENT().esxi_host_virtual_switch+"\" }",
"variable \"workload_datastore\" { default = \""+config.E2EP_ENVIRONMENT().esxi_host_datastore+"\" }",
"variable \"compute_host\" {default = \""+config.E2EP_ENVIRONMENT().esxi_host_ip+"\"}",
"variable \"vsphere_server\" {default = \""+config.VCSA().ip+"\"}",
"variable \"vsphere_user\" { default = \""+config.VCSA().username+"\"}",
"variable \"vsphere_password\" { default = \""+config.UNIVERSAL().password+"\"}",
"variable \"mgmt_pg\" { default = \""+config.E2EP_ENVIRONMENT().esxi_host_virtual_switch+"\" }",
"variable \"vm_name\" { default = \""+config.NSX().nsx_vm_name+"\" }",
"variable \"local_ovf_path\" { default = \"/usr/local/drop/"+config.NSX().nsx_ova_source+"\" }",
"variable \"deployment_option\" { default = \""+config.NSX().mgrformfactor+"\" }",
"variable \"nsx_role\" { default = \"NSX Manager\" }",
"variable \"nsx_ip_0\" { default = \""+config.NSX().ip+"\" }",
"variable \"nsx_netmask_0\" { default = \""+config.E2EP_ENVIRONMENT().subnet_mask+"\" }",
"variable \"nsx_gateway_0\" { default = \""+config.E2EP_ENVIRONMENT().default_gw+"\" }",
"variable \"nsx_dns1_0\" { default = \""+config.DNS().ip+"\" }",
"variable \"nsx_domain_0\" { default = \""+config.DNS().zone+"\" }",
"variable \"nsx_ntp_0\" { default = \""+config.E2EP_ENVIRONMENT().ntp_server+"\" }",
"variable \"nsx_isSSHEnabled\" { default = \"True\" }",
"variable \"nsx_allowSSHRootLogin\" { default = \"True\" }",
"variable \"nsx_passwd_0\" { default = \""+config.NSX().password+"\" }",
"variable \"nsx_cli_passwd_0\" { default = \""+config.NSX().password+"\" }",
"variable \"nsx_cli_audit_passwd_0\" { default = \""+config.NSX().password+"\" }",
"variable \"nsx_hostname\" { default = \""+config.NSX().fqdn+"\" }"
]

tf_var_file_name = "nsx_var.tf"
tf_var_file_exists = exists(tf_var_file_name)
if tf_var_file_exists:
    err = "    removing old nsx_vars.tf file"
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
