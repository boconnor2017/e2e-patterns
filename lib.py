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

def change_vm_ip_address(vm_name, new_ip, new_subnet, new_df_gw):
    docker_rm = True
    docker_entrypoint = "/usr/bin/pwsh"
    docker_volume = {os.getcwd():{'bind':'/tmp', 'mode':'rw'}}
    docker_image = "vmware/powerclicore"
    docker_cmd = "/tmp/change-vm-ip.ps1 \""
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


def change_vm_os_password(vm_name, new_vm_password):
    docker_entrypoint = "/usr/bin/pwsh"
    docker_volume = {os.getcwd():{'bind':'/tmp', 'mode':'rw'}}
    docker_image = "vmware/powerclicore"
    docker_cmd = "/tmp/change-photon_default_pw.ps1 \'"
    docker_cmd = docker_cmd+config.E2EP_ENVIRONMENT().esxi_host_ip+" "
    docker_cmd = docker_cmd+config.E2EP_ENVIRONMENT().esxi_host_username+" "
    docker_cmd = docker_cmd+config.E2EP_ENVIRONMENT().esxi_host_password+" "
    docker_cmd = docker_cmd+vm_name+" "
    docker_cmd = docker_cmd+new_vm_password+"\'"
    dclient = docker.from_env()
    dclient.containers.run(image=docker_image, entrypoint=docker_entrypoint, volumes=docker_volume, remove=True, command=docker_cmd)

def connect_to_ssh_server_test(ip, un, pw):
    try:
        pclient = paramiko.SSHClient()
        pclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        pclient.connect(hostname=ip, username=un, password=pw)
        pclient.close()
        return True
    except:
        pclient.close()
        return False

def send_command_over_ssh(cmd, ip, un, pw):
    pclient = paramiko.SSHClient()
    pclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    pclient.connect(hostname=ip, username=un, password=pw)
    stdin, stdout, stderr = pclient.exec_command(cmd, timeout=None)
    stdout=stdout.readlines()
    pclient.close()
    return stdout

def download_photon_prep_script_via_ssh(ip, un, pw):
    cmd = "curl https://raw.githubusercontent.com/boconnor2017/e2e-patterns/main/prep-photon.sh >> /usr/local/prep-photon.sh"
    send_command_over_ssh(cmd, ip, un, pw)

def build_photon_controller(vm_name, vm_source, logfile_name):
    class VM():
        name = vm_name 
        source = vm_source 
    
    err = ""
    write_to_logs(err, logfile_name)
    err = "Running download_photon_prep_script_via_ssh()"
    write_to_logs(err, logfile_name)
    err = "VM() Class:"
    write_to_logs(err, logfile_name)
    err = "    .name: "+VM().name
    write_to_logs(err, logfile_name)
    err = "    .source: "+VM().source
    write_to_logs(err, logfile_name)
    err = ""
    write_to_logs(err, logfile_name)
    err = "Building generic photon appliance:"
    write_to_logs(err, logfile_name)
    err = build_photon_with_ovftool_container(VM().name, VM().source)
    write_to_logs(err, logfile_name)
    err = ""
    seconds = (60*2)
    err = "Pausing for "+str(seconds)+" seconds to let the ova to complete its build..."
    write_to_logs(err, logfile_name)
    pause_python_for_duration(seconds)
    err = "Resuming script."
    write_to_logs(err, logfile_name)
    err = ""
    write_to_logs(err, logfile_name)
    err = "Changing the default password using powercli container."
    write_to_logs(err, logfile_name)
    change_vm_os_password(VM().name, config.E2EP_ENVIRONMENT().photonos_password)
    seconds = (20)
    err = "Pausing for "+str(seconds)+" seconds to let the password change to take effect..."
    write_to_logs(err, logfile_name)
    pause_python_for_duration(seconds)
    err = "Resuming script."
    write_to_logs(err, logfile_name)
    err = ""
    write_to_logs(err, logfile_name)
    err = "Getting ip address:"
    write_to_logs(err, logfile_name)
    photon_ip_address = get_vm_ip_address(VM().name)
    err = "    IP Address: "+photon_ip_address
    write_to_logs(err, logfile_name)
    err = ""
    write_to_logs(err, logfile_name)
    err = "Testing SSH connection to "+photon_ip_address
    write_to_logs(err, logfile_name)
    ssh_test = connect_to_ssh_server_test(photon_ip_address, config.E2EP_ENVIRONMENT().photonos_username, config.E2EP_ENVIRONMENT().photonos_password)
    if ssh_test:
        err = "   connection succeeded."
        write_to_logs(err, logfile_name)
    else:
        err = "[!] connection failed"
        write_to_logs(err, logfile_name)
    err = ""
    write_to_logs(err, logfile_name)
    if ssh_test:
        err = "Downloading photon prep scripts."
        write_to_logs(err, logfile_name)
        download_photon_prep_script_via_ssh(photon_ip_address, config.E2EP_ENVIRONMENT().photonos_username, config.E2EP_ENVIRONMENT().photonos_password)
        err = ""
        write_to_logs(err, logfile_name)
    if ssh_test:
        err = "Pulling prep script into variable"
        write_to_logs(err, logfile_name)
        prep_photon_script_source = "/usr/local/prep-photon.sh"
        prep_photon_script_txt = populate_var_from_file(prep_photon_script_source)
        prep_photon_script_commands = prep_photon_script_txt.split('\n')
        err = "Validating Commands:"
        write_to_logs(err, logfile_name)
        i=0
        for commands in prep_photon_script_commands:
            err = "    ["+str(i)+"] "+commands
            write_to_logs(err, logfile_name)
            i=i+1
    err = ""
    write_to_logs(err, logfile_name)
    if ssh_test:
        err = "Pulling prep script into variable"
        write_to_logs(err, logfile_name)
        prep_photon_script_source = "/usr/local/prep-photon.sh"
        prep_photon_script_txt = populate_var_from_file(prep_photon_script_source)
        prep_photon_script_commands = prep_photon_script_txt.split('\n')
        err = "Running Commands:"
        write_to_logs(err, logfile_name)
        i=0
        for commands in prep_photon_script_commands:
            err = "    Running: ["+str(i)+"] "+commands
            write_to_logs(err, logfile_name)
            stdout = send_command_over_ssh(commands, photon_ip_address, config.E2EP_ENVIRONMENT().photonos_username, config.E2EP_ENVIRONMENT().photonos_password)
            i=i+1
    err = "Finished."
    write_to_logs(err, logfile_name)
