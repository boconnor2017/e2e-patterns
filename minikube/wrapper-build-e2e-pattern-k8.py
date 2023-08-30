# Deploys a Minikube Pattern
# Author: Brendan O'Connor
# Date: August 2023
# Add python script (example below)
import os
import shutil
import sys
import paramiko
import docker

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
logfile_name = config.LOGS().minikube
err = "Starting wrapper-build-e2e-pattern-photon.py"
lib.write_to_logs(err, logfile_name)
err = "Input variables:"
lib.write_to_logs(err, logfile_name)
i=0 
for args in sys.argv:
	err = "    "+args[i]
	lib.write_to_logs(err, logfile_name)
	i=i+1

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


# Virtual Machine Details
class VM():
	name = sys.argv[1] # as displayed in vCenter
	source = sys.argv[2] # (syntax: ova-name.ova)
	prep_script = "/usr/local/e2e-patterns/minikube/install-minikube.sh"


# Run /usr/local/e2e-patterns/photon/build-e2e-pattern-controller.sh 

# Get IP Address
src_file = '/usr/local/e2e-patterns/photon/get-vm-ip.ps1'
des_dir = os.getcwd()
err = "Retrieving get-vm-ip file from "+src_file+" and copying to "+des_dir
lib.write_to_logs(err, logfile_name)
outpt = shutil.copy(src_file, des_dir)
err = ""
lib.write_to_logs(err, logfile_name)
err = "Running get_vm_ip_address("+VM().name+")"
lib.write_to_logs(err, logfile_name)
photon_ip_address = get_vm_ip_address(VM().name)
err = "    ip address: "+photon_ip_address
lib.write_to_logs(err, logfile_name)

# Create commands for PhotonOS paramiko configuration
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
for command_validate in photon_prep_run_script:
	err = "    ["+str(i)+"] "+command_validate
	lib.write_to_logs(err, logfile_name)
	i=i+1

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
retry = 0
ssh_to_photon(client, photon_ip_address, config.E2EP_ENVIRONMENT().photonos_username, config.E2EP_ENVIRONMENT().photonos_password, retry)

# Execute prep scripts to PhotonOS
err = "Executing photon prep scripts:"
lib.write_to_logs(err, logfile_name)
run_ssh_command(photon_prep_run_script)
err = ""
lib.write_to_logs(err, logfile_name)

# Close SSH Session
client.close()
