# Builds a photon controller (a prepped photon appliance ready for building patterns)
# 	Deploy photon: uses ovftool container
#	Change password: uses powercli container
#	Get IP address (DHCP assigned): uses powercli container
#	Configure photon: uses paramiko to ssh into the os 
# Author: Brendan O'Connor
# Date: August 2023

import os
import shutil
import paramiko
import docker
import subprocess
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

import config
import lib

# Start log file
logfile_name = config.LOGS().photonos
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
err = "Starting wrapper-build-e2e-pattern-photon-2.py"
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Functions 
def run_ssh_command(run_cmd):
	i=0
	for command in run_cmd:
	    err = "    ["+str(i)+"] "+command
	    lib.write_to_logs(err, logfile_name)
	    stdin, stdout, stderr = client.exec_command(command, timeout=None)
	    err = (stdout.read().decode())
	    lib.write_to_logs(err, logfile_name)
	    err = stderr.read().decode()
	    lib.write_to_logs(err, logfile_name)
	    err = ""
	    lib.write_to_logs(err, logfile_name)
	    i=i+1

def get_vm_ip_address(vm_name):
	docker_rm = True
	docker_entrypoint = "/usr/bin/pwsh"
	docker_volume = {os.getcwd():{'bind':'/tmp', 'mode':'rw'}}
	docker_image = "vmware/powerclicore"
	docker_cmd = "/tmp/get-vm-ip.ps1 \""+config.E2EP_ENVIRONMENT().esxi_host_ip+" "+config.E2EP_ENVIRONMENT().esxi_host_username+" "+config.E2EP_ENVIRONMENT().esxi_host_password+" "+vm_name+"\""
	client = docker.from_env()
	ip_address_raw = client.containers.run(image=docker_image, entrypoint=docker_entrypoint, volumes=docker_volume, remove=docker_rm, command=docker_cmd)
	ip_address_raw = str(ip_address_raw)
	ip_address = ip_address_raw[-17:-5]
	return ip_address

def ssh_to_photon(client, ip, un, pw, retry):
    err = "Attempting connection to the SSH Server:"
	lib.write_to_logs(err, logfile_name)
	err = "    ip: "+ip 
	lib.write_to_logs(err, logfile_name)
	err = "    username: "+un 
	lib.write_to_logs(err, logfile_name)
	err = "    password: "+pw 
	lib.write_to_logs(err, logfile_name)
	if retry < 5:
		try: 
			client.connect(hostname=ip, username=un, password=pw)
		except:
			err = "[!] Cannot connect to the SSH Server"
			lib.write_to_logs(err, logfile_name)
			seconds = (10)
			err = "Pausing for "+str(seconds)+" seconds before retry number "+str(retry)
			lib.write_to_logs(err, logfile_name)
			retry=retry+1
			ssh_to_photon(client, ip, un, pw, retry)
	else:
		err = "[!] Cannot connect to the SSH Server"
		lib.write_to_logs(err, logfile_name)
		err = "Closing connection."
		lib.write_to_logs(err, logfile_name)
		exit()

# Virtual Machine Details
class VM():
	name = sys.argv[1] # as displayed in vCenter
	source = sys.argv[2] # (syntax: ova-name.ova)
	prep_script = "/usr/local/prep-photon.sh"
	refresh_script = "/usr/local/refresh-e2e-patterns.sh"

err = "VM() Class:"
lib.write_to_logs(err, logfile_name)
err = "    .name: "+VM().name
lib.write_to_logs(err, logfile_name)
err = "    .source: "+VM().source
lib.write_to_logs(err, logfile_name)
err = "    .prep_scrip: "+VM().prep_script
lib.write_to_logs(err, logfile_name)
err = "    .refresh_script: "+VM().refresh_script
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Deploy Photon Appliance using ovftool container
err = "Deploying photon machine: "+VM().name+" "+VM().source
lib.write_to_logs(err, logfile_name)
subprocess.run(["sh", "build-e2e-pattern-photon.sh", VM().name, VM().source])

# Pause to allow password change to take effect 
seconds = (60*2)
err = "Pausing for "+str(seconds)+" seconds to let the ova to complete its build..."
lib.write_to_logs(err, logfile_name)
lib.pause_python_for_duration(seconds)
err = "Resuming script."
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Get IP Address of the photon vm
err = "Getting ip address:"
lib.write_to_logs(err, logfile_name)
photon_ip_address = get_vm_ip_address(VM().name)
err = "    IP Address: "+photon_ip_address
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Configure password using powercli container
err = "Configure password using pcli container:"
lib.write_to_logs(err, logfile_name)
docker_rm = True 
docker_entrypoint = "/usr/bin/pwsh"
docker_volume = {os.getcwd():{'bind':'/tmp', 'mode':'rw'}}
docker_image = "vmware/powerclicore"
docker_cmd = "/tmp/configure-photon.ps1 \""+config.E2EP_ENVIRONMENT().esxi_host_ip+" "+config.E2EP_ENVIRONMENT().esxi_host_username+" "+config.E2EP_ENVIRONMENT().esxi_host_password+" "+VM().name+" "+config.E2EP_ENVIRONMENT().photonos_password+"\""
err = "    docker_cmd: "+docker_cmd
lib.write_to_logs(err, logfile_name)
client = docker.from_env()
client.containers.run(image=docker_image, entrypoint=docker_entrypoint, volumes=docker_volume, remove=docker_rm, command=docker_cmd)
err = ""
lib.write_to_logs(err, logfile_name)

# Pause to allow password change to take effect 
seconds = 30
err = "Pausing for "+str(seconds)+" seconds to let password change to take effect..."
lib.write_to_logs(err, logfile_name)
lib.pause_python_for_duration(seconds)
err = "Resuming script."
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Create commands for PhotonOS paramiko configuration
photon_prep_downloads = [
    "curl https://raw.githubusercontent.com/boconnor2017/e2e-patterns/main/prep-photon.sh >> "+VM().prep_script,
    "curl https://raw.githubusercontent.com/boconnor2017/e2e-patterns/main/refresh-e2e-patterns.sh >> "+VM().refresh_script
]

with open(VM().prep_script) as file:
	txt = file.read()

photon_prep_run_script = txt.split('\n')

# Connect to SSH Host
err = "Connecting to ssh host "+photon_ip_address
lib.write_to_logs(err, logfile_name)

# Validate commands
err = "Validating commands:"
lib.write_to_logs(err, logfile_name)
i=0
for command_validate in photon_prep_downloads:
	err = "    ["+str(i)+"] "+command_validate
	lib.write_to_logs(err, logfile_name)
	i=i+1

err = ""
lib.write_to_logs(err, logfile_name)
i=0
for command_validate in photon_prep_run_script:
	err = "    ["+str(i)+"] "+command_validate
	lib.write_to_logs(err, logfile_name)
	i=i+1

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
retry = 0
ssh_to_photon(client, photon_ip_address, config.E2EP_ENVIRONMENT().photonos_username, config.E2EP_ENVIRONMENT().photonos_password, retry)

# Download scripts to PhotonOS
err = "Downloading scripts to Photon from github:"
lib.write_to_logs(err, logfile_name)
run_ssh_command(photon_prep_downloads)
err = ""
lib.write_to_logs(err, logfile_name)

# Execute prep scripts to PhotonOS
err = "Executing photon prep scripts:"
lib.write_to_logs(err, logfile_name)
run_ssh_command(photon_prep_run_script)
err = ""
lib.write_to_logs(err, logfile_name)

# Close SSH Session
client.close()
err = "Finished. SSH Session closed."
lib.write_to_logs(err, logfile_name)
