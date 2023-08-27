# Configure PhotonOS using PowerCLI container
# Author: Brendan O'Connor
# Date: August 2023
import os
import shutil
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
logfile_name = config.LOGS().photonos
err = "Starting wrapper-build-e2e-pattern-photon-2.py"
lib.write_to_logs(err, logfile_name)

# Parameters
pcli_source = "configure-photon.ps1"
err = "powercli source: "+pcli_source
lib.write_to_logs(err, logfile_name)

# Run PowerCLI container 
docker_rm = True 
docker_entrypoint = "/usr/bin/pwsh"
docker_volume = {os.getcwd():{'bind':'/tmp', 'mode':'rw'}}
docker_image = "vmware/powerclicore"
docker_cmd = "/tmp/configure-photon.ps1 \""+config.E2EP_ENVIRONMENT().esxi_host_ip+" "+config.E2EP_ENVIRONMENT().esxi_host_username+" "+config.E2EP_ENVIRONMENT().esxi_host_password+" "+config.E2EP_ENVIRONMENT().photonos_username+" "+config.E2EP_ENVIRONMENT().photonos_password+"\""

err = "docker run parameters:"
lib.write_to_logs(err, logfile_name)
err = "    docker_image: "+docker_image
lib.write_to_logs(err, logfile_name)
err = "    docker_rm: "+str(docker_rm)
lib.write_to_logs(err, logfile_name)
err = "    docker_entrypoint: "+docker_entrypoint
lib.write_to_logs(err, logfile_name)
err = "    docker_volumes: "+str(docker_volume)
lib.write_to_logs(err, logfile_name)
err = "    docker_cmd: "+docker_cmd
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)
err = "executing docker run command..."
lib.write_to_logs(err, logfile_name)

client = docker.from_env()
client.containers.run(image=docker_image, entrypoint=docker_entrypoint, volumes=docker_volume, remove=docker_rm, command=docker_cmd)
err = "Finished! If the results are different than expected, troubleshoot the ps1 script directly."
lib.write_to_logs(err, logfile_name)
