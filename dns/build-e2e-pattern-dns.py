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
logfile_name = config.LOGS().dns
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
err = "Starting build-e2e-pattern-dns.py"
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
    04. Check remote service status http://config.DNS().ip:5380 
    05. First time login: admin/admin > get token 
    06. Change password config.DNS().password 
    07. Retrieve new token
    08. Create e2e.local zone 
    09. Add records to e2e.local zone from config.E2E_IPAM()
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

# Pause to allow network config to take effect
seconds = 10
err = "Pausing for "+str(seconds)+" to allow networking configuration to take effect."
lib.write_to_logs(err, logfile_name)
lib.pause_python_for_duration(seconds)
err = "Resuming script."
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Validating Configure IP Tables 
configure_tanium_ip_tables_script = os.getcwd()+"/configure-tanium-ip-tables.sh"
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
    lib.send_command_over_ssh(command, config.DNS().ip, config.E2EP_ENVIRONMENT().photonos_username, config.E2EP_ENVIRONMENT().photonos_password)
    i=i+1
err = ""
lib.write_to_logs(err, logfile_name)

# Pause to allow network config to take effect
seconds = 10
err = "Pausing for "+str(seconds)+" seconds to allow networking configuration to take effect."
lib.write_to_logs(err, logfile_name)
lib.pause_python_for_duration(seconds)
err = "Resuming script."
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Validating Install Technitium script 
run_docker_compose_script = os.getcwd()+"/run-docker-compose.sh"
err = "Pulling scripts from "+run_docker_compose_script
lib.write_to_logs(err, logfile_name)
run_docker_compose_raw = lib.populate_var_from_file(run_docker_compose_script)
run_docker_compose_commands = run_docker_compose_raw.split('\n')
err = ""
lib.write_to_logs(err, logfile_name)
err = "Validating commands:"
lib.write_to_logs(err, logfile_name)
i=0
for command in run_docker_compose_commands:
    err = "    ["+str(i)+"] "+command
    lib.write_to_logs(err, logfile_name)
    i=i+1
err = ""
lib.write_to_logs(err, logfile_name)

# Run Install Technitium script
err = "Configuring Tanium IP Tables:"
lib.write_to_logs(err, logfile_name)
i=0
for command in run_docker_compose_commands:
    err = "    ["+str(i)+"] "+command
    lib.write_to_logs(err, logfile_name)
    lib.send_command_over_ssh(command, config.DNS().ip, config.E2EP_ENVIRONMENT().photonos_username, config.E2EP_ENVIRONMENT().photonos_password)
    i=i+1
err = ""
lib.write_to_logs(err, logfile_name)

# Pause to allow Technitium to finish install
seconds = 60
err = "Pausing for "+str(seconds)+" seconds to allow Technitium to complete its install."
lib.write_to_logs(err, logfile_name)
lib.pause_python_for_duration(seconds)
err = "Resuming script."
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)
# Check web service status
dns_web_service_url = "http://"+config.DNS().ip+":"+config.DNS().port
err = "Checking web service status:"
lib.write_to_logs(err, logfile_name)
retry = 0
retry_max = 5
retry_pause = 10
dns_web_service_status = lib.check_web_service_status(dns_web_service_url, retry, retry_max, retry_pause)
err = "    return code: "+str(dns_web_service_status)
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Get token, first time login using admin/admin credentials
err = "First time API call to DNS server using admin/admin credentials."
lib.write_to_logs(err, logfile_name)
api_url = "http://"+config.DNS().ip+":"+config.DNS().port+"/api/user/login?user=admin&pass=admin&includeInfo=true"
err = "    url: "+api_url
lib.write_to_logs(err, logfile_name)
api_response = lib.api_get(api_url)
err = "    json: "+str(api_response.json())
lib.write_to_logs(err, logfile_name)
api_token = (api_response.json()['token'])
err = "    token: "+api_token
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Change default password
# Syntax: http://localhost:5380/api/user/changePassword?token=x&pass=password
err = "Change default password"
lib.write_to_logs(err, logfile_name)
api_url = "http://"+config.DNS().ip+":"+config.DNS().port+"/api/user/changePassword?token="+api_token+"&pass="+config.UNIVERSAL().password
err = "    url: "+api_url
lib.write_to_logs(err, logfile_name)
err = "    new password: "+config.UNIVERSAL().password
lib.write_to_logs(err, logfile_name)
api_response = lib.api_get(api_url)
err = "    api response: "+str(api_response.json())
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Get new token using permanent password
err = "Get token with permanent password."
lib.write_to_logs(err, logfile_name)
api_url = "http://"+config.DNS().ip+":"+config.DNS().port+"/api/user/login?user=admin&pass="+config.UNIVERSAL().password+"&includeInfo=true"
err = "    url: "+api_url
lib.write_to_logs(err, logfile_name)
api_response = lib.api_get(api_url)
err = "    json: "+str(api_response.json())
lib.write_to_logs(err, logfile_name)
api_token = (api_response.json()['token'])
err = "    token: "+api_token
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Create DNS zone 
# Syntax: http://localhost:5380/api/zones/create?token=x&zone=example.com&type=Primary
err = "Create "+config.DNS().zone+" zone."
lib.write_to_logs(err, logfile_name)
api_url = "http://"+config.DNS().ip+":"+config.DNS().port+"/api/zones/create?token="+api_token+"&zone="+config.DNS().zone+"&type=Primary"
err = "    url: "+api_url
lib.write_to_logs(err, logfile_name)
api_response = lib.api_get(api_url)
err = "    api response: "+str(api_response.json())
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Add records to DNS zone
err = "Adding records to "+config.DNS().zone+" zone:"
lib.write_to_logs(err, logfile_name)

i=0
for x in config.IPAM().tag:
    err = "    ["+str(i)+"] tag: "+config.IPAM().tag[i]
    lib.write_to_logs(err, logfile_name)
    err = "    ["+str(i)+"] fqdn: "+config.IPAM().fqdn[i]
    lib.write_to_logs(err, logfile_name)
    err = "    ["+str(i)+"] ip: "+config.IPAM().ip[i]
    lib.write_to_logs(err, logfile_name)
    api_response = lib.create_dns_record(api_token, config.IPAM().fqdn[i], config.DNS().zone, config.IPAM().ip[i])
    err = "    api response: "+str(api_response.json())
    lib.write_to_logs(err, logfile_name)
    i=i+1

err = ""
lib.write_to_logs(err, logfile_name)
err = "Finished."
lib.write_to_logs(err, logfile_name)
