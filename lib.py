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

def build_photon_with_ovftool_container(vm_name, vm_source):
    docker_image = "ovftool" 
    docker_volume = {"/usr/local/drop":{'bind':'/root/home', 'mode':'rw'}}
    docker_cmd = "--sourceType=OVA "
    docker_cmd = docker_cmd+"--acceptAllEulas "
    docker_cmd = docker_cmd+"--allowExtraConfig "
    docker_cmd = docker_cmd+"--noSSLVerify "
    docker_cmd = docker_cmd+"--diskMode=thin "
    docker_cmd = docker_cmd+"--powerOn "
    docker_cmd = docker_cmd+"--datastore='"+config.E2EP_ENVIRONMENT().esxi_host_datastore+"' "
    docker_cmd = docker_cmd+"--network='"+config.E2EP_ENVIRONMENT().esxi_host_virtual_switch+"' "
    docker_cmd = docker_cmd+"--name='"+vm_name+"' "
    docker_cmd = docker_cmd+"'"+vm_source+"' "
    docker_cmd = docker_cmd+"vi://'"+config.E2EP_ENVIRONMENT().esxi_host_username+"':'"+config.E2EP_ENVIRONMENT().esxi_host_password+"'@"+config.E2EP_ENVIRONMENT().esxi_host_ip
    dclient = docker.from_env()
    err = dclient.containers.run(image=docker_image, volumes=docker_volume, tty=True, working_dir="/root/home", remove=True, command=docker_cmd)
    return str(err)

