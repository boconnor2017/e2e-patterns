# Description: vCenter Server from a Photon controller
# Author: Brendan O'Connor
# Date: September 2023
# Version: 2.0

# Base imports
import os
import shutil
import sys
import json

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
logfile_name = config.LOGS().vcsa
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
err = "Starting build-e2e-pattern-vcenter-server.py"
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

# Check for input parameters
err = "Checking for input parameters:"
lib.write_to_logs(err, logfile_name)
err = "    parameters: "+sys.argv[1]
lib.write_to_logs(err, logfile_name)
if sys.argv[1] == "-p":
    skip_build_photon_controller = True
    err = "    skipping build photon controller"
    lib.write_to_logs(err, logfile_name)
else:
    skip_build_photon_controller = False

# Build photon controller
if skip_build_photon_controller:
    skip_build_photon_controller = True 
else:
    err = "Building photon controller:"
    lib.write_to_logs(err, logfile_name)
    lib.build_photon_controller(config.VCSA().photon_controller_vm_name, config.VCSA().photon_source, logfile_name)
    err = ""
    lib.write_to_logs(err, logfile_name)

# Get Photon controller IP
err = "Getting IP address of photon controller:"
lib.write_to_logs(err, logfile_name)
photon_controller_ip_address = lib.get_vm_ip_address(config.VCSA().photon_controller_vm_name)
err = "    ip address: "+photon_controller_ip_address
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

'''
vCenter Build Process:
01. Create photon controller using naming convention from config file
02. Create directory /usr/local/mount
03. MANUAL: attach the vcenter iso to the photon controller
04. Mount the iso to the /mount directory 
05. Create DNS entries for the new vCSA
06. Generate JSON for vcenter using config file
07. Run the installer using Paramiko 
08: Get vcenter api session id
09. Configure datacenter using info from config file 
'''

# Create directory /usr/local/mount
err = "Creating mount directory."
lib.write_to_logs(err, logfile_name)
create_dir_cmd = "mkdir /usr/local/mount"
err = "    command: "+create_dir_cmd
lib.write_to_logs(err, logfile_name)
lib.send_command_over_ssh(create_dir_cmd, photon_controller_ip_address, config.E2EP_ENVIRONMENT().photonos_username, config.E2EP_ENVIRONMENT().photonos_password)
err = ""
lib.write_to_logs(err, logfile_name)

# Prompt user to continue with script
if skip_build_photon_controller:
    skip_build_photon_controller = True 
else:
    err = "Prompting user and pausing until the ISO is attached to the photon controller..."
    lib.write_to_logs(err, logfile_name)
    print("")
    print("")
    print("This next step requires manual intervention.")
    print("Attach the vCenter ISO to the photon controller (vm name: "+config.VCSA().photon_controller_vm_name+")")
    pressanykeytocontinue = input("Press Enter to continue:")
    print("")
    print("")
    err = "Prompt received. Continuing with the script. "
    lib.write_to_logs(err, logfile_name)
    err = ""
    lib.write_to_logs(err, logfile_name)

# Mount ISO to the photon controller 
err = "Mounting ISO:"
lib.write_to_logs(err, logfile_name)
mount_iso_cmd = "mount -t iso9660 -o loop /dev/cdrom /usr/local/mount/"
err = "    command: "+mount_iso_cmd
lib.write_to_logs(err, logfile_name)
lib.send_command_over_ssh(mount_iso_cmd, photon_controller_ip_address, config.E2EP_ENVIRONMENT().photonos_username, config.E2EP_ENVIRONMENT().photonos_password)
err = ""
lib.write_to_logs(err, logfile_name)

# List DNS zones
err = "Validating "+config.DNS().zone+" zone."
lib.write_to_logs(err, logfile_name)
dns_token = lib.get_dns_token()
err = "    token: "+dns_token
lib.write_to_logs(err, logfile_name)
api_response = lib.get_dns_zones(dns_token)
err = "    api response: "+str(api_response.json())
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Create DNS Record
err = "Creating DNS Record:"
lib.write_to_logs(err, logfile_name)
dns_token = lib.get_dns_token()
err = "    token: "+dns_token
lib.write_to_logs(err, logfile_name)
err = "    ip: "+config.VCSA().ip
lib.write_to_logs(err, logfile_name)
api_response = lib.create_dns_record(dns_token, config.VCSA().domain_hostname, config.DNS().zone, config.VCSA().ip)
err = "    api response: "+str(api_response.json())
lib.write_to_logs(err, logfile_name)
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Generate JSON for vCenter configuration 
err = "Generating JSON for vCenter configuration."
lib.write_to_logs(err, logfile_name)
vcsa_config_json_as_string = {
    "__version": "2.13.0",
    "__comments": "https://github.com/boconnor2017/e2e-patterns",
    "new_vcsa": {
        "esxi": {
            "hostname": config.E2EP_ENVIRONMENT().esxi_host_ip,
            "username": config.E2EP_ENVIRONMENT().esxi_host_username,
            "password": config.E2EP_ENVIRONMENT().esxi_host_password,
            "deployment_network": config.E2EP_ENVIRONMENT().esxi_host_virtual_switch,
            "datastore": config.E2EP_ENVIRONMENT().esxi_host_datastore
        },
        "appliance": {
            "__comments": [
                "E2E Pattern: deploy vcsa"
            ],
            "thin_disk_mode": True,
            "deployment_option": "small",
            "name": config.VCSA().vcsa_vm_name
        },
        "network": {
            "ip_family": "ipv4",
            "mode": "static",
            "system_name": config.VCSA().fqdn,
            "ip": config.VCSA().ip,
            "prefix": config.E2EP_ENVIRONMENT().subnet_size,
            "gateway": config.E2EP_ENVIRONMENT().default_gw,
            "dns_servers": [
                config.DNS().ip
            ]
        },
        "os": {
            "password": config.UNIVERSAL().password,
            "ntp_servers": config.E2EP_ENVIRONMENT().ntp_server,
            "ssh_enable": False
        },
        "sso": {
            "password": config.UNIVERSAL().password,
            "domain_name": config.VCSA().sso_domain
        }
    },
    "ceip": {
        "description": {
            "__comments": [
                "E2E Pattern"
            ]
        },
        "settings": {
            "ceip_enabled": True
        }
    }
}

vcsa_config_json = json.dumps(vcsa_config_json_as_string)
err = ""
lib.write_to_logs(err, logfile_name)
err = "Validating json:"
lib.write_to_logs(err, logfile_name)
err = "    json: "+vcsa_config_json
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Write json to file
if skip_build_photon_controller:
    skip_build_photon_controller = True 
    err = "Cleaning up old json config file."
    cmd = "rm "+config.VCSA().json_filename
    err = "    cmd: "+cmd
    lib.write_to_logs(err, logfile_name)
    stdout = lib.send_command_over_ssh(cmd, photon_controller_ip_address, config.E2EP_ENVIRONMENT().photonos_username, config.E2EP_ENVIRONMENT().photonos_password)
    err = ""
    lib.write_to_logs(err, logfile_name)

err = "Writing json to file on the photon controller:"
lib.write_to_logs(err, logfile_name)
err = "    filename: "+config.VCSA().json_filename
lib.write_to_logs(err, logfile_name)
cmd = "echo \'"+vcsa_config_json+"\' >> "+config.VCSA().json_filename
err = "    cmd: "+cmd
lib.write_to_logs(err, logfile_name)
stdout = lib.send_command_over_ssh(cmd, photon_controller_ip_address, config.E2EP_ENVIRONMENT().photonos_username, config.E2EP_ENVIRONMENT().photonos_password)

# Create vCenter
err = "Creating vCenter:"
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Pause to allow build to complete
seconds = (60*25)
lib.create_new_vcenter(logfile_name, photon_controller_ip_address, config.E2EP_ENVIRONMENT().photonos_username, config.E2EP_ENVIRONMENT().photonos_password, seconds)

# Get vCenter API session ID 
def retry_vc(retry, max_retry, pause_seconds):
    err = "    Retry: "+str(retry)
    lib.write_to_logs(err, logfile_name)
    if retry < max_retry:
        try:
            vc_session_id = lib.get_vc_session_id(config.VCSA().fqdn, config.VCSA().username, config.UNIVERSAL().password)
            return vc_session_id
        except:
            err = "    [!] Failed on retry "+str(retry)+" of "+max_retry 
            lib.write_to_logs(err, logfile_name)
            retry = retry+1
            lib.pause_python_for_duration(pause_seconds)
            retry_vc(retry, max_retry, pause_seconds)
    else:
        err = "    [!] Max retry exceeded."
        lib.write_to_logs(err, logfile_name)
        vc_session_id = ""
        return vc_session_id

err = "Getting vCenter Session ID:"
retry = 0
max_retry = 20
pause_seconds = (60*3)
lib.write_to_logs(err, logfile_name)
vc_session_id = retry_vc(retry, max_retry, pause_seconds)
lib.write_to_logs(err, logfile_name)
err = "    session id: "+vc_session_id
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Configure datacenter 
err = "Creating Datacenter:"
lib.write_to_logs(err, logfile_name)
err = "    session id: "+vc_session_id 
lib.write_to_logs(err, logfile_name)
err = "    VCSA FQDN: "+config.VCSA().fqdn
lib.write_to_logs(err, logfile_name)
err = "    VCSA datacenter: "+config.VCSA().datacenter
vc_datacenter = lib.create_vc_datacenter(vc_session_id, config.VCSA().fqdn, config.VCSA().datacenter)
err = str(vc_datacenter)
lib.write_to_logs(err, logfile_name)
