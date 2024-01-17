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

def docker_ovftool_deploy_photon(vm_name):
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
    docker_cmd = docker_cmd+"'"+config.PHOTONOS().source+"' "
    docker_cmd = docker_cmd+"vi://'"+config.E2EP_ENVIRONMENT().esxi_host_username+"':'"+config.E2EP_ENVIRONMENT().esxi_host_password+"'@"+config.E2EP_ENVIRONMENT().esxi_host_ip
    dclient = docker.from_env()
    err = dclient.containers.run(image=docker_image, volumes=docker_volume, tty=True, working_dir="/root/home", remove=True, command=docker_cmd)
    return str(err)

def docker_powercli_change_default_photonos_password(vm_name, new_vm_password):
    download_file_from_github(config.SCRIPTS().change_photonos_default_password_with_powercli_url, config.SCRIPTS().change_photonos_default_password_with_powercli_filename) 
    docker_entrypoint = "/usr/bin/pwsh"
    docker_volume = {os.getcwd():{'bind':'/tmp', 'mode':'rw'}}
    docker_image = "vmware/powerclicore"
    docker_cmd = "/tmp/"+config.SCRIPTS().change_photonos_default_password_with_powercli_filename+" \'"
    docker_cmd = docker_cmd+config.E2EP_ENVIRONMENT().esxi_host_ip+" "
    docker_cmd = docker_cmd+config.E2EP_ENVIRONMENT().esxi_host_username+" "
    docker_cmd = docker_cmd+config.E2EP_ENVIRONMENT().esxi_host_password+" "
    docker_cmd = docker_cmd+vm_name+" "
    docker_cmd = docker_cmd+new_vm_password+"\'"
    dclient = docker.from_env()
    dclient.containers.run(image=docker_image, entrypoint=docker_entrypoint, volumes=docker_volume, remove=True, command=docker_cmd)


def docker_powercli_change_vm_ip_address(vm_name, new_ip, new_subnet, new_df_gw):
    download_file_from_github(config.SCRIPTS().change_vm_ip_with_powercli_url, config.SCRIPTS().change_vm_ip_with_powercli_filename) 
    docker_rm = True
    docker_entrypoint = "/usr/bin/pwsh"
    docker_volume = {os.getcwd():{'bind':'/tmp', 'mode':'rw'}}
    docker_image = "vmware/powerclicore"
    docker_cmd = "/tmp/"+config.SCRIPTS().change_vm_ip_with_powercli_filename+" \""
    docker_cmd = docker_cmd+config.E2EP_ENVIRONMENT().esxi_host_ip+" "
    docker_cmd = docker_cmd+config.E2EP_ENVIRONMENT().esxi_host_username+" "
    docker_cmd = docker_cmd+config.E2EP_ENVIRONMENT().esxi_host_password+" "
    docker_cmd = docker_cmd+vm_name+" "
    docker_cmd = docker_cmd+new_ip+" "
    docker_cmd = docker_cmd+new_subnet+" "
    docker_cmd = docker_cmd+new_df_gw+" "
    docker_cmd = docker_cmd+"\""
    dclient = docker.from_env()
    dclient.containers.run(image=docker_image, entrypoint=docker_entrypoint, volumes=docker_volume, remove=docker_rm, command=docker_cmd)


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

def docker_powercli_get_vm_ip_address(vm_name):
    download_file_from_github(config.SCRIPTS().get_vm_ip_with_powercli_url, config.SCRIPTS().get_vm_ip_with_powercli_filename) 
    docker_rm = True
    docker_entrypoint = "/usr/bin/pwsh"
    docker_volume = {os.getcwd():{'bind':'/tmp', 'mode':'rw'}}
    docker_image = "vmware/powerclicore"
    docker_cmd = "/tmp/"+config.SCRIPTS().get_vm_ip_with_powercli_filename+" \""+config.E2EP_ENVIRONMENT().esxi_host_ip+" "+config.E2EP_ENVIRONMENT().esxi_host_username+" "+config.E2EP_ENVIRONMENT().esxi_host_password+" "+vm_name+"\""
    dclient = docker.from_env()
    ip_address_raw = dclient.containers.run(image=docker_image, entrypoint=docker_entrypoint, volumes=docker_volume, remove=docker_rm, command=docker_cmd)
    ip_address_raw = str(ip_address_raw)
    ip_address = ip_address_raw[-17:-5]
    ip_address = ip_address.replace("n", "")
    ip_address = ip_address.replace("\\", "")
    return ip_address

def paramiko_download_file_to_remote_photon_vm(ip, un, pw, url, filepath, filename):
    # filepath format: /foo/bar/
    # filename format: somefile.xyz
    cmd = "curl "+url+" >> "+filepath+filename
    paramiko_send_command_over_ssh(cmd, ip, un, pw)

def paramiko_send_command_over_ssh(cmd, ip, un, pw):
    pclient = paramiko.SSHClient()
    pclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    pclient.connect(hostname=ip, username=un, password=pw)
    stdin, stdout, stderr = pclient.exec_command(cmd, timeout=None)
    stdout=stdout.readlines()
    pclient.close()
    return stdout

def run_local_shell_cmd(cmd):
    err = subprocess.run(cmd, capture_output=True)
    return err

def write_to_logs(err, logfile_name):
    tstamp = str(datetime.now())
    logfile = open(logfile_name, "a")
    logfile.write(tstamp+": "+err+" \n")
    logfile.close
