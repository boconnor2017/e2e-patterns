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
# docker run --rm --entrypoint="/usr/bin/pwsh" -v ${PWD}:/tmp vmware/powerclicore /tmp/configure-photon.ps1 "172.16.0.201 root VMware1! root VMware1!VMware1!" 

docker_rm = True 
docker_entrypoint = "/usr/bin/pwsh"
docker_volume = {os.getcwd():{'bind':'/tmp', 'mode':'rw'}}
docker_image = "vmware/powerclicore"
docker_cmd = "/tmp/configure-photon.ps1 \"172.16.0.201 root VMware1! root VMware1!VMware1!\""
client = docker.from_env()
client.containers.run(image=docker_image, entrypoint=docker_entrypoint, volumes=docker_volume, remove=docker_rm, command=docker_cmd)

