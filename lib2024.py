# E2E Patterns Python Library 2024
# Author: Brendan O'Connor
# Date: January 2024
# Version: 3.0
# Reference: https://github.com/boconnor2017/e2e-patterns

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

def download_file_from_github(url, filename):
    urllib.request.urlretrieve(url, filename)

def e2e_patterns_header(logfile_name, pattern_name):
    err = ""
    write_to_logs(err, logfile_name)
    err = "-----------------------------------------------------"
    write_to_logs(err, logfile_name)
    err = "-----------------------------------------------------"
    write_to_logs(err, logfile_name)
    err = "-----------------------------------------------------"
    write_to_logs(err, logfile_name)
    err = "WELCOME TO E2E PATTERNS 2024!"
    write_to_logs(err, logfile_name)
    err = "-----------------------------------------------------"
    write_to_logs(err, logfile_name)
    err = "-----------------------------------------------------"
    write_to_logs(err, logfile_name)
    err = "-----------------------------------------------------"
    write_to_logs(err, logfile_name)
    err = "Starting build of pattern "+pattern_name
    write_to_logs(err, logfile_name)
    err = "Author: Brendan O'Connor"
    write_to_logs(err, logfile_name)
    err = ""
    write_to_logs(err, logfile_name)

def write_to_logs(err, logfile_name):
    tstamp = str(datetime.now())
    logfile = open(logfile_name, "a")
    logfile.write(tstamp+": "+err+" \n")
    logfile.close

def docker_powercli_create_vm(vm_name):
    download_file_from_github(config.SCRIPTS().create_vm_with_powercli_url, config.SCRIPTS().create_vm_with_powercli_filename)
    docker_rm = True
    docker_image = "vmware/powerclicore"
    docker_entrypoint = "/usr/bin/pwsh"
    docker_volume = {os.getcwd():{'bind':'/tmp', 'mode':'rw'}}
    docker_cmd = "/tmp/"+config.SCRIPTS().create_vm_with_powercli_filename+" \""
    docker_cmd = docker_cmd+config.E2EP_ENVIRONMENT().esxi_host_ip+" "
    docker_cmd = docker_cmd+config.E2EP_ENVIRONMENT().esxi_host_username+" "
    docker_cmd = docker_cmd+config.E2EP_ENVIRONMENT().esxi_host_password+" "
    docker_cmd = docker_cmd+vm_name+"\""
    dclient = docker.from_env()
    err = dclient.containers.run(image=docker_image, entrypoint=docker_entrypoint, volumes=docker_volume, remove=True, command=docker_cmd)
    return err

def run_local_shell_cmd(cmd):
    err = subprocess.run(cmd, capture_output=True)
    return err

# TEST 04!!!
