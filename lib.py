# E2E Patterns Python Library
# Author: Brendan O'Connor
# Date: September 2023

import requests
import urllib3
import urllib
import shutil
import time
import json
import os
import docker 
import paramiko
import docker
import subprocess
import sys
from vmware.vapi.vsphere.client import create_vsphere_client
from datetime import datetime
import config

## GENERIC PYTHON
def pause_python_for_duration(seconds):
    time.sleep(seconds)

## E2E LOGGING
def write_to_logs(err, logfile_name):
    tstamp = str(datetime.now())
    logfile = open(logfile_name, "a")
    logfile.write(tstamp+": "+err+" \n")
    logfile.close

## DOCKER FUNCTIONS
def get_vm_ip_address(vm_name):
	docker_rm = True
	docker_entrypoint = "/usr/bin/pwsh"
	docker_volume = {os.getcwd():{'bind':'/tmp', 'mode':'rw'}}
	docker_image = "vmware/powerclicore"
	docker_cmd = "/tmp/get-vm-ip.ps1 \""+config.E2EP_ENVIRONMENT().esxi_host_ip+" "+config.E2EP_ENVIRONMENT().esxi_host_username+" "+config.E2EP_ENVIRONMENT().esxi_host_password+" "+vm_name+"\""
	dclient = docker.from_env()
	ip_address_raw = dclient.containers.run(image=docker_image, entrypoint=docker_entrypoint, volumes=docker_volume, remove=docker_rm, command=docker_cmd)
	ip_address_raw = str(ip_address_raw)
	ip_address = ip_address_raw[-17:-5]
	return ip_address

def deploy_photon_ovftool_container():
    #TODO: replace wrapper-build-e2e-pattern-photon.py

## PARAMIKO (SSH) FUNCTIONS
def ssh_to_photon(ip, un, pw, retry):
    pclient = paramiko.SSHClient()
    pclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	if retry < 5:
		try: 
			err = pclient.connect(hostname=ip, username=un, password=pw)
            return str(err)
		except:
			seconds = (10)
			retry=retry+1
			ssh_to_photon(ip, un, pw, retry)
            err = "[!] Cannot connect to the SSH Server"
            return err

	else:
		err = "[!] Cannot connect to the SSH Server"
        exit()
        return err
