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
    err = "    01A. Prompt user to upload nested appliance to /usr/local/drop."
    lib.write_to_logs(err, logfile_name)
    print("Please ensure "+config.NESTED_ESXI8().nested_esxi8_ova_source+" is uploaded to "+ip_address+".")
    continue_with_script = input("When confirmed, press <ENTER> to continue...")
    print("Continuing with the script.")
    err = "    01A. Continuing with the script."
    lib.write_to_logs(err, logfile_name)
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

# 03. Cleanup existing tf files from node controller
err = "03. Cleanup existing tf files from node controller started."
lib.write_to_logs(err, logfile_name)
filepath = fullpath+"/"
filename = config.SCRIPTS().build_nested_esxi8_main_tf_filename
err = "    03A. Removing "+filepath+filename
lib.write_to_logs(err, logfile_name)
lib.paramiko_delete_file_from_remote_photon_vm(ip_address, config.PHOTONOS().username, config.PHOTONOS().password, filepath, filename)
filename = "var.tf"
err = "    03B. Removing "+filepath+filename
lib.write_to_logs(err, logfile_name)
lib.paramiko_delete_file_from_remote_photon_vm(ip_address, config.PHOTONOS().username, config.PHOTONOS().password, filepath, filename)
filepath = "/usr/local/drop/"
filename = "main.tf"
err = "    03C. Removing "+filepath+filename
lib.write_to_logs(err, logfile_name)
lib.paramiko_delete_file_from_remote_photon_vm(ip_address, config.PHOTONOS().username, config.PHOTONOS().password, filepath, filename)
filename = "var.tf"
err = "    03D. Removing "+filepath+filename
lib.write_to_logs(err, logfile_name)
lib.paramiko_delete_file_from_remote_photon_vm(ip_address, config.PHOTONOS().username, config.PHOTONOS().password, filepath, filename)
filepath = fullpath+"/"
filename = "_tf_init.log"
err = "    03E. Removing "+filepath+filename
lib.write_to_logs(err, logfile_name)
lib.paramiko_delete_file_from_remote_photon_vm(ip_address, config.PHOTONOS().username, config.PHOTONOS().password, filepath, filename)
filename = "_tf_plan.log"
err = "    03F. Removing "+filepath+filename
lib.write_to_logs(err, logfile_name)
lib.paramiko_delete_file_from_remote_photon_vm(ip_address, config.PHOTONOS().username, config.PHOTONOS().password, filepath, filename)
filename = "_tf_apply.log"
err = "    03G. Removing "+filepath+filename
lib.write_to_logs(err, logfile_name)
lib.paramiko_delete_file_from_remote_photon_vm(ip_address, config.PHOTONOS().username, config.PHOTONOS().password, filepath, filename)
err = "03. Cleanup existing tf files from node controller finished."
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# 04. Download main.tf to node controller 
err = "04. Download main.tf to node controller started."
lib.write_to_logs(err, logfile_name)
err = "    Node Controller IP: "+ip_address
lib.write_to_logs(err, logfile_name)
err = "    main.tf URL: "+config.SCRIPTS().build_nested_esxi8_main_tf_url
lib.write_to_logs(err, logfile_name)
filepath = fullpath+"/"
err = "    Filepath where main.tf is being dropped: "+filepath
lib.write_to_logs(err, logfile_name)
err = "    03B. Downloading main.tf."
lib.write_to_logs(err, logfile_name)
stdout = lib.paramiko_download_file_to_remote_photon_vm(ip_address, config.PHOTONOS().username, config.PHOTONOS().password, config.SCRIPTS().build_nested_esxi8_main_tf_url, filepath, config.SCRIPTS().build_nested_esxi8_main_tf_filename)
err = "03. Download main.tf to node controller finished."
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# 05. Create terraform variables file 
err = "05. Create terraform variables file started."
lib.write_to_logs(err, logfile_name)
tf_var_txt = ["# Python generated var file",
"variable \"vsphere_user\" { default = \""+config.VCSA().username+"\" }",
"variable \"vsphere_pass\" { default = \""+config.UNIVERSAL().password+"\" }",
"variable \"vsphere_serer\" { default = \""+config.VCSA().ip+"\" }",
"variable \"datacenter_name\" { default = \""+config.VCSA().datacenter+"\" }",
"variable \"datastore_name\" { default = \""+config.E2EP_ENVIRONMENT().esxi_host_datastore+"\" }",
"variable \"network_name\" { default = \""+config.E2EP_ENVIRONMENT().esxi_host_virtual_switch+"\" }",
"variable \"esxi_host_name\" { default = \""+config.E2EP_ENVIRONMENT().esxi_host_ip+"\" }",
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
"variable \"guest_password\" { default = \""+config.E2EP_ENVIRONMENT().ntp_server+"\" }",
"variable \"local_ovf_path\" { default = \""+config.NESTED_ESXI8().nested_esxi8_ova_source+"\" }"
]

var_file_name = "var.tf"
var_file_exists = exists(var_file_name)
if var_file_exists:
    err = "    removing old var file"
    lib.write_to_logs(err, logfile_name)
    os.remove(var_file_name)

for line in tf_var_txt:
    lib.append_text_to_file(line+"\n", var_file_name)

err = "05. Create terraform variables file finished."
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# 06. Move terraform variable file to node controller 
err = "06. Move terraform variable file to node controller started."
lib.write_to_logs(err, logfile_name)
err = "    06A. Populating variable using var.tf."
lib.write_to_logs(err, logfile_name)
file_as_var = lib.populate_var_from_file('var.tf')
err = "    06B. Moving var.tf to node controller."
lib.write_to_logs(err, logfile_name)
stdout = lib.paramiko_move_file_to_remote_photon_vm(ip_address, config.PHOTONOS().username, config.PHOTONOS().password, file_as_var, filepath, 'var.tf')
err = "06. Move terraform variable file to node controller finished."
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# 05. Run Terraform on node controller 
# (cp /usr/local/e2e-patterns/vcf/main.tf /usr/local/drop/main.tf; cp /usr/local/e2e-patterns/vcf/var.tf /usr/local/drop/var.tf; cd /usr/local/drop; docker run -v $(pwd):$(pwd) -w $(pwd) -i -t hashicorp/terraform init >> /usr/local/e2e-patterns/vcf/_tf_init.log)
# (cd /usr/local/drop; docker  run  -v $(pwd):$(pwd) -w $(pwd) -i -t hashicorp/terraform plan >> /usr/local/e2e-patterns/vcf/_tf_plan.log)
# (cd /usr/local/drop; docker  run  -v $(pwd):$(pwd) -w $(pwd) -i -t hashicorp/terraform apply -auto-approve  >> /usr/local/e2e-patterns/vcf/_tf_apply.log)

err = "05. Run Terraform on node controller started."
lib.write_to_logs(err, logfile_name)
err = "    05A. Running Terraform init command."
lib.write_to_logs(err, logfile_name)
cmd = "(cp /usr/local/e2e-patterns/vcf/main.tf /usr/local/drop/main.tf; cp /usr/local/e2e-patterns/vcf/var.tf /usr/local/drop/var.tf; cd /usr/local/drop; docker run -v $(pwd):$(pwd) -w $(pwd) -i -t hashicorp/terraform init >> /usr/local/e2e-patterns/vcf/_tf_init.log)"
err = "    05A. cmd: "+cmd
lib.write_to_logs(err, logfile_name)
lib.paramiko_send_command_over_ssh(cmd, ip_address, config.PHOTONOS().username, config.PHOTONOS().password)
lib.write_to_logs(err, logfile_name)
seconds = 30
err = "    05A. pausing script for "+str(seconds)+" seconds."
lib.write_to_logs(err, logfile_name)
lib.pause_python_for_duration(seconds)
err = "    05A. Resuming script."
lib.write_to_logs(err, logfile_name)

err = "    05B. Running Terraform plan command."
lib.write_to_logs(err, logfile_name)
cmd = "(cd /usr/local/drop; docker  run  -v $(pwd):$(pwd) -w $(pwd) -i -t hashicorp/terraform plan >> /usr/local/e2e-patterns/vcf/_tf_plan.log)"
err = "    05B. cmd: "+cmd
lib.write_to_logs(err, logfile_name)
lib.paramiko_send_command_over_ssh(cmd, ip_address, config.PHOTONOS().username, config.PHOTONOS().password)
lib.write_to_logs(err, logfile_name)
seconds = 30
err = "    05B. pausing script for "+str(seconds)+" seconds."
lib.write_to_logs(err, logfile_name)
lib.pause_python_for_duration(seconds)
err = "    05B. Resuming script."
lib.write_to_logs(err, logfile_name)

err = "    05C. Running Terraform apply command."
lib.write_to_logs(err, logfile_name)
cmd = "(cd /usr/local/drop; docker  run  -v $(pwd):$(pwd) -w $(pwd) -i -t hashicorp/terraform apply -auto-approve  >> /usr/local/e2e-patterns/vcf/_tf_apply.log)"
err = "    05C. cmd: "+cmd
lib.write_to_logs(err, logfile_name)
lib.paramiko_send_command_over_ssh(cmd, ip_address, config.PHOTONOS().username, config.PHOTONOS().password)
lib.write_to_logs(err, logfile_name)
seconds = 30
err = "    05C. pausing script for "+str(seconds)+" seconds."
lib.write_to_logs(err, logfile_name)
lib.pause_python_for_duration(seconds)
err = "    05C. Resuming script."
lib.write_to_logs(err, logfile_name)

err = "05. Run Terraform on node controller finished."
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)
