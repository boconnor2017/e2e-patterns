# Description: Installs Tanium (DNS container service) on a Photon controller
# Author: Brendan O'Connor
# Date: September 2023
# Version: 2.0

# Base imports
import os
import shutil
import sys

# Get pattern config file
src_file = '/usr/local/e2e-patterns/config.py'
des_dir = os.getcwd()
print("Retrieving config file from "+src_file+" and copying to "+des_dir)
outpt = shutil.copy(src_file, des_dir)
print(str(outpt))
print("")

# Get pattern library
src_file = '/usr/local/e2e-patterns/lib.py'
des_dir = os.getcwd()
print("Retrieving library file from "+src_file+" and copying to "+des_dir)
outpt = shutil.copy(src_file, des_dir)
print(str(outpt))
print("")

# Import pattern config and library
import config
import lib

# Start log file
logfile_name = config.LOGS().minikube
err = ""
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)
err = "* * * * * * * * * * * * * * * * * * * * * * * * * * * * *"
lib.write_to_logs(err, logfile_name)
err = "* * * * * * * * * * * * * * * * * * * * * * * * * * * * *"
lib.write_to_logs(err, logfile_name)
err = "Starting build-e2e-pattern-minikube.py"
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Photon controller prerequisites
err = "Photon controller prerequisites:"
lib.write_to_logs(err, logfile_name)
src_file = '/usr/local/e2e-patterns/photon/change-photon_default_pw.ps1'
des_dir = os.getcwd()
err = "    copying "+src_file+" and copying to "+des_dir
outpt = shutil.copy(src_file, des_dir)
src_file = '/usr/local/e2e-patterns/photon/get-vm-ip.ps1'
des_dir = os.getcwd()
err = "    copying "+src_file+" and copying to "+des_dir
outpt = shutil.copy(src_file, des_dir)
src_file = '/usr/local/e2e-patterns/photon/change-vm-ip.ps1'
des_dir = os.getcwd()
err = "    copying "+src_file+" and copying to "+des_dir
outpt = shutil.copy(src_file, des_dir)
err = ""
lib.write_to_logs(err, logfile_name)

# Build photon controller
lib.build_photon_controller(config.DNS().vm_name, config.DNS().photon_source, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Get VM IP
err = "Getting IP address of photon controller:"
lib.write_to_logs(err, logfile_name)
ip_address = lib.get_vm_ip_address(config.DNS().vm_name)
err = "    ip address: "+ip_address
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

'''
DNS Server Installation process:
    01. Change VM IP address using change-vm-ip.ps1 with pcli container
    02. Configure IP tables using paramiko and configure-tanium-ip-tables.sh script
    03. Install Technitium Container using paramiko and run-docker-compose.sh script
    04. Check local service status http://localhost:5380 
    05. Check remote service status http://config.DNS().ip:5380 
    06. First time login: admin/admin > get token 
    07. Change password config.DNS().password 
    08. Retrieve new token
    09. Create e2e.local zone 
    10. Add records to e2e.local zone from config.E2E_IPAM()
'''

# Change VM IP 
err = "Changing "+config.DNS().vm_name+" Networking:"
lib.write_to_logs(err, logfile_name)
err = "    ip address: "+config.DNS().ip
lib.write_to_logs(err, logfile_name)
err = "    subnet: "+config.E2EP_ENVIRONMENT().subnet_mask
lib.write_to_logs(err, logfile_name)
err = "    default gateway: "+config.E2EP_ENVIRONMENT().default_gw
lib.write_to_logs(err, logfile_name)
lib.change_vm_ip_address(config.DNS().vm_name, config.DNS().ip, config.E2EP_ENVIRONMENT().subnet_mask, config.E2EP_ENVIRONMENT().default_gw)
err = ""
lib.write_to_logs(err, logfile_name)

# Validating Configure IP Tables 
configure_tanium_ip_tables_script = os.getcwd()+"/configure-tanium-ip-tables.sh.sh"
err = "Pulling scripts from "+configure_tanium_ip_tables_script
lib.write_to_logs(err, logfile_name)
configure_tanium_ip_tables_raw = lib.populate_var_from_file(configure_tanium_ip_tables_script)
configure_tanium_ip_tables_commands = configure_tanium_ip_tables_raw.split('\n')
err = ""
lib.write_to_logs(err, logfile_name)
err = "Validating commands:"
lib.write_to_logs(err, logfile_name)
i=0
for command in configure_tanium_ip_tables_commands:
    err = "    ["+str(i)+"] "+command
    lib.write_to_logs(err, logfile_name)
    i=i+1
err = ""
lib.write_to_logs(err, logfile_name)

# Configuring IP Tables
err = "Configuring Tanium IP Tables:"
lib.write_to_logs(err, logfile_name)
i=0
for command in configure_tanium_ip_tables_commands:
    err = "    ["+str(i)+"] "+command
    lib.write_to_logs(err, logfile_name)
    lib.send_command_over_ssh(command, ip_address, E2EP_ENVIRONMENT().photonos_username, E2EP_ENVIRONMENT().photonos_password)
    i=i+1
err = ""
lib.write_to_logs(err, logfile_name)

# THE REST

err = "Finished."
lib.write_to_logs(err, logfile_name)
