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

def populate_var_from_file(file_name):
    with open(file_name) as file:
        file_txt = file.read()
        return file_txt

## E2E LOGGING
def write_to_logs(err, logfile_name):
    tstamp = str(datetime.now())
    logfile = open(logfile_name, "a")
    logfile.write(tstamp+": "+err+" \n")
    logfile.close

# E2E LIBRARY

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

def change_vm_os_password(vm_name, new_vm_password):
    dclient = docker.from_env()
    docker_entrypoint = "/usr/bin/pwsh"
    docker_volume = {os.getcwd():{'bind':'/tmp', 'mode':'rw'}}
    docker_image = "vmware/powerclicore"
    docker_cmd = "/tmp/configure-photon.ps1 \" "
    docker_cmd = docker_cmd+config.E2EP_ENVIRONMENT().esxi_host_ip+" "
    docker_cmd = docker_cmd+config.E2EP_ENVIRONMENT().esxi_host_username+" "
    docker_cmd = docker_cmd+config.E2EP_ENVIRONMENT().esxi_host_password+" "
    docker_cmd = docker_cmd+vm_name+" "
    docker_cmd = docker_cmd+new_vm_password+"\""
    err = dclient.containers.run(image=docker_image, entrypoint=docker_entrypoint, volumes=docker_volume, remove=True, command=docker_cmd)
    return err 

def connect_to_ssh_server(pclient, ip, un, pw):
    try:
        pclient.connect(hostname=ip, username=un, password=pw)
        err = 1
        return err
    except:
        err = 0
        return err

def send_command_over_ssh(cmd, ip, un, pw):
    pclient = paramiko.SSHClient()
    pclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connect_to_ssh_server(pclient, ip, un, pw)
    pclient.exec_command(cmd, timeout=None)
    pclient.close()

def download_photon_prep_script_via_ssh(ip, un, pw):
    cmd = "curl https://raw.githubusercontent.com/boconnor2017/e2e-patterns/main/prep-photon.sh >> /usr/local/prep-photon.sh"
    send_command_over_ssh(cmd, ip, un, pw)
