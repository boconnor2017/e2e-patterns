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


# Virtual Machine Details
class VM():
	name = sys.argv[1] # as displayed in vCenter
	source = sys.argv[2] # (syntax: ova-name.ova)
	prep_script = "/usr/local/prep-photon.sh"
	refresh_script = "/usr/local/refresh-e2e-patterns.sh"


# Deploy Photon Appliance using ovftool container
print("TEMPORARY: in the future this will deploy photon.")

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

# Get IP Address of the new photon os by name using powercli container
photon_ip_address = "172.16.0.138"

# Pause to allow password change to take effect 
seconds = 30
err = "Pausing for "+str(seconds)+" to let password change to take effect..."
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
try:
    client.connect(hostname=photon_ip_address, username=config.E2EP_ENVIRONMENT().photonos_username, password=config.E2EP_ENVIRONMENT().photonos_password)
except:
    print("[!] Cannot connect to the SSH Server")
    exit()

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
