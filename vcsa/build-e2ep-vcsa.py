# Description: Builds vCenter on an ESXi host
# Author: Brendan O'Connor
# Date: January 2024
# Version: 3.0

# lib and config filenames for the year 
# Must be available in /e2e-patterns repository
lib_filename = "lib2024.py"
config_filename = "config2024.py"

# Base imports
import os
import shutil
import json

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
logfile_name = config.LOGS().vcsa
pattern_name = config.VCSA().pattern
lib.e2e_patterns_header(logfile_name, pattern_name)
err = ""
lib.write_to_logs(err, logfile_name)

# 01. Check for node controller
err = "01. Check for node controller started."
lib.write_to_logs(err, logfile_name)
node_controller_exists = lib.e2e_check_for_node_controller(config.VCSA().photon_controller_vm_name)
if node_controller_exists == 1:
    err = "    "+config.VCSA().photon_controller_vm_name+" exists."
    lib.write_to_logs(err, logfile_name)
else:
    err = "    "+config.VCSA().photon_controller_vm_name+" does not exist."
    lib.write_to_logs(err, logfile_name)
    err = "    Running e2e_build_node_controller()."
    lib.write_to_logs(err, logfile_name)
    lib.e2e_build_node_controller(config.VCSA().photon_controller_vm_name, logfile_name)
err = "01. Check for node controller finished."
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# 02. Get IP Address of the node controller 
err = "02. Get IP Address of the node controller started."
lib.write_to_logs(err, logfile_name)
ip_address = lib.docker_powercli_get_vm_ip_address(config.VCSA().photon_controller_vm_name)
err = "    IP Address of "+config.VCSA().photon_controller_vm_name+" is "+ip_address
lib.write_to_logs(err, logfile_name)
err = "02. Get IP Address of the node controller finished."
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# 03. Create mount directory on node controller
err = "03. Create mount directory on node controller started."
lib.write_to_logs(err, logfile_name)
if node_controller_exists == 1:
    err = "Skipping 03. Create mount directory on node controller."
    lib.write_to_logs(err, logfile_name)
else:
    cmd = "mkdir /usr/local/mount"
    stdout = lib.paramiko_send_command_over_ssh(cmd, ip_address, config.PHOTONOS().username, config.PHOTONOS().password)
err = "03. Create mount directory on node controller finished."
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# 04. Attach VCSA ISO to node controller
err = "04. Attach VCSA ISO to node controller started."
lib.write_to_logs(err, logfile_name)
if node_controller_exists == 1:
    err = "Skipping 04. Attach VCSA ISO to node controller."
    lib.write_to_logs(err, logfile_name)
else:
    lib.docker_powercli_attach_iso_to_vm(config.VCSA().photon_controller_vm_name, config.E2EP_ENVIRONMENT().esxi_host_datastore, config.VCSA().iso_folder_on_datastore, config.VCSA().iso_name)
    mount_iso_cmd = "mount -t iso9660 -o loop /dev/cdrom /usr/local/mount/"
    stdout = lib.paramiko_send_command_over_ssh(mount_iso_cmd, ip_address, config.PHOTONOS().username, config.PHOTONOS().password)
err = "04. Attach VCSA ISO to node controller finished."
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# 05. Create DNS Record
err = "05. Create DNS Record started."
lib.write_to_logs(err, logfile_name)
err = "    05A. Generating Tanium Token."
lib.write_to_logs(err, logfile_name)
tanium_token = lib.tanium_get_token('admin', config.UNIVERSAL().password)
err = "    05A. Tanium Token: "+tanium_token
lib.write_to_logs(err, logfile_name)
err = "    05B. Creating DNS Record: "+config.VCSA().domain_hostname+" "+config.VCSA().ip
lib.write_to_logs(err, logfile_name)
lib.tanium_create_dns_record(tanium_token, config.VCSA().domain_hostname, config.DNS().zone, config.VCSA().ip)
err = "05. Create DNS Record finished."
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# 06. Generate JSON File for vCenter Configuration
err = "06. Generate JSON File for vCenter Configuration started."
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
err = "06. Generate JSON File for vCenter Configuration finished."
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# 07. Write JSON file to node controller using paramiko
err = "07. Write JSON file to node controller using paramiko started."
lib.write_to_logs(err, logfile_name)
lib.paramiko_move_file_to_remote_photon_vm(ip_address, config.PHOTONOS().username, config.PHOTONOS().password, vcsa_config_json, config.VCSA().json_filepath, config.VCSA().json_filename)
err = "07. Write JSON file to node controller using paramiko finished."
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# 08. Install vCenter
err = "08. Install vCenter started."
lib.write_to_logs(err, logfile_name)
lib.e2e_install_vCenter_using_node_controller(ip_address, logfile_name)
err = "08. Install vCenter started."
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)
