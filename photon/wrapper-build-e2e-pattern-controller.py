# Run photon prep script remotely from master controller
# Author: Brendan O'Connor
# Date: August 2023
import os
import shutil
import paramiko
import docker
import subprocess

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

# Parameters
photon_host = "172.16.0.136"
photon_vm_name = "e2ep-photontest-11"
photon_prep_source = "/usr/local/prep-photon.sh"
photon_refresh_source = "/usr/local/refresh-e2e-patterns.sh" 

# Configure password using powercli container
err = "Configure password using pcli container:"
lib.write_to_logs(err, logfile_name)
docker_rm = True 
docker_entrypoint = "/usr/bin/pwsh"
docker_volume = {os.getcwd():{'bind':'/tmp', 'mode':'rw'}}
docker_image = "vmware/powerclicore"
docker_cmd = "/tmp/configure-photon.ps1 \""+config.E2EP_ENVIRONMENT().esxi_host_ip+" "+config.E2EP_ENVIRONMENT().esxi_host_username+" "+config.E2EP_ENVIRONMENT().esxi_host_password+" "+photon_vm_name+" "+config.E2EP_ENVIRONMENT().photonos_password+"\""
err = "    docker_cmd: "+docker_cmd
lib.write_to_logs(err, logfile_name)
client = docker.from_env()
client.containers.run(image=docker_image, entrypoint=docker_entrypoint, volumes=docker_volume, remove=docker_rm, command=docker_cmd)
err = ""
lib.write_to_logs(err, logfile_name)

# Pause to allow password change to take effect 
seconds = 30
err = "Pausing for "+str(seconds)+" to let password change to take effect..."
lib.write_to_logs(err, logfile_name)
lib.pause_python_for_duration(seconds)
err = "Resuming script."
lib.write_to_logs(err, logfile_name)

# Create commands for PhotonOS
photon_prep_downloads = [
    "curl https://raw.githubusercontent.com/boconnor2017/e2e-patterns/main/prep-photon.sh >> /usr/local/prep-photon.sh",
    "curl https://raw.githubusercontent.com/boconnor2017/e2e-patterns/main/refresh-e2e-patterns.sh >> /usr/local/refresh-e2e-patterns.sh"
]

with open(photon_prep_source) as file:
	txt = file.read()

photon_prep_run_script = txt.split('\n')

# Connect to SSH Host
err = "Connecting to ssh host "+photon_host
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
    client.connect(hostname=photon_host, username=config.E2EP_ENVIRONMENT().photonos_username, password=config.E2EP_ENVIRONMENT().photonos_password)
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
