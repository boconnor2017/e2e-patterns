# E2E Patterns Python Library
# Author: Brendan O'Connor
# Date: September 2023
# Version: 2.0

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

def write_text_to_file(text, file_name):
    new_file = open(file_name, "w")
    new_file.writelines(text)
    new_file.close()

def check_web_service_status(web_svc_url, retry, retry_max, retry_pause):
    if retry < retry_max:
        try:
            return_code = urllib.request.urlopen(web_svc_url).getcode()
            return return_code 
        except:
            pause_python_for_duration(retry_pause)
            retry = retry+1
            return_code = check_web_service_status(web_svc_url, retry, retry_max, retry_pause)
            return return_code
    else:
        return "[!] Web service check failed "+str(retry_max)+" times."

def api_get(api_url):
    api_response = requests.get(api_url)
    return api_response

## E2E LOGGING
def write_to_logs(err, logfile_name):
    tstamp = str(datetime.now())
    logfile = open(logfile_name, "a")
    logfile.write(tstamp+": "+err+" \n")
    logfile.close

def e2e_patterns_header(logfile_name, pattern_name):
    err = ""
    write_to_logs(err, logfile_name)
    err = "-----------------------------------------------------"
    write_to_logs(err, logfile_name)
    err = "-----------------------------------------------------"
    write_to_logs(err, logfile_name)
    err = "-----------------------------------------------------"
    write_to_logs(err, logfile_name)
    err = "WELCOME TO E2E PATTERNS!"
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

def get_dns_token():
    api_url = "http://"+config.DNS().ip+":"+config.DNS().port+"/api/user/login?user=admin&pass="+config.UNIVERSAL().password+"&includeInfo=true"
    api_response = api_get(api_url)
    api_token = (api_response.json()['token'])
    return api_token

# Syntax: http://localhost:5380/api/zones/create?token=x&zone=example.com&type=Primary
def create_dns_zone(token):
    api_url = "http://"+config.DNS().ip+":"+config.DNS().port+"/api/zones/create?"
    api_url = api_url+"token="+token
    api_url = api_url+"&zone="+config.DNS().zone
    api_url = api_url+"&type=Primary"
    api_url = api_url+"&forwarder=this-server"
    api_response = api_get(api_url)
    return api_response

def get_dns_zones(token):
    api_url = "http://"+config.DNS().ip+":"+config.DNS().port+"/api/zones/list?"
    api_url = api_url+"token="+token
    api_response = api_get(api_url)
    return api_response

# Syntax: http://localhost:5380/api/zones/records/add?token=x&domain=example.com&zone=example.com
def create_dns_record(token, domain_name, zone, ip):
    api_url = "http://"+config.DNS().ip+":"+config.DNS().port+"/api/zones/records/add?"
    api_url = api_url+"token="+token
    api_url = api_url+"&domain="+domain_name+"."+zone
    api_url = api_url+"&zone="+zone
    api_url = api_url+"&type=A"
    api_url = api_url+"&ttl=3600"
    api_url = api_url+"&overwrite=true"
    api_url = api_url+"&ipAddress="+ip
    api_url = api_url+"&ptr=true"
    api_url = api_url+"&createPtrZone=true"
    api_response = api_get(api_url)
    return api_response 

def create_new_vcenter(logfile_name, ip, un, pw, pause_seconds):
    err = "def create_new_vcenter("+logfile_name+", "+ip+", "+un+", "+pw+", "+str(pause_seconds)
    write_to_logs(err, logfile_name)    
    run_vcsa_installer_cmd = "sh /usr/local/mount/vcsa-cli-installer/lin64/./vcsa-deploy "
    run_vcsa_installer_cmd = run_vcsa_installer_cmd+"install "+config.VCSA().json_filename+" "
    run_vcsa_installer_cmd = run_vcsa_installer_cmd+"--accept-eula --acknowledge-ceip --no-ssl-certificate-verification "
    run_vcsa_installer_cmd = run_vcsa_installer_cmd+">> /usr/local/e2e-patterns/vcsa/__vcsa-deploy.log"
    err = "    run_vcsa_installer_cmd: "+run_vcsa_installer_cmd
    write_to_logs(err, logfile_name)    
    pclient = paramiko.SSHClient()
    pclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    pclient.connect(hostname=ip, username=un, password=pw)
    pclient.exec_command(run_vcsa_installer_cmd, timeout=None)
    pclient.close()
    err = "Command sent to SSH host. Pausing for "+str(pause_seconds)+" seconds to allow VCSA install to complete."
    write_to_logs(err, logfile_name)  
    pause_python_for_duration(pause_seconds)
    err = "Resuming script. Exiting create_new_vcenter()."
    write_to_logs(err, logfile_name)  
    err = ""
    write_to_logs(err, logfile_name)
    
def get_vc_session_id(vcenter_hostname, vcenter_username, vcenter_password):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    sess = requests.post("https://"+vcenter_hostname+"/rest/com/vmware/cis/session", auth=(vcenter_username, vcenter_password), verify=False)
    session_id = sess.json()['value']
    return(session_id)

def create_vc_datacenter(session_id, vcenter_hostname, datacenter_name):
    api_call = requests.post("https://"+vcenter_hostname+"/api/vcenter/datacenter", verify=False, headers={
    "vmware-api-session-id": session_id
    }, json={
    "folder": "group-d1",
    "name": datacenter_name
    })
    datacenter = api_call.json()
    return datacenter

def build_nsx_with_ovftool_container():
    docker_image = "ovftool" 
    docker_volume = {"/usr/local/drop":{'bind':'/root/home', 'mode':'rw'}}
    docker_cmd = "--noSSLVerify --skipManifestCheck --powerOn "
    docker_cmd = docker_cmd+"--deploymentOption="+config.NSX().mgrformfactor+" "
    docker_cmd = docker_cmd+"--diskMode=thin "
    docker_cmd = docker_cmd+"--acceptAllEulas "
    docker_cmd = docker_cmd+"--allowExtraConfig "
    docker_cmd = docker_cmd+"--ipProtocol=IPv4 "
    docker_cmd = docker_cmd+"--ipAllocationPolicy=fixedPolicy "
    docker_cmd = docker_cmd+"--datastore='"+config.E2EP_ENVIRONMENT().esxi_host_datastore+"' "
    docker_cmd = docker_cmd+"--network='"+config.E2EP_ENVIRONMENT().esxi_host_virtual_switch+"' "
    docker_cmd = docker_cmd+"--name='"+config.NSX().nsx_vm_name+"' "
    docker_cmd = docker_cmd+"--prop:nsx_hostname='"+config.NSX().domain_hostname+"' "
    docker_cmd = docker_cmd+"--prop:nsx_role='NSX Manager' "
    docker_cmd = docker_cmd+"--prop:nsx_ip_0='"+config.NSX().ip+"' "
    docker_cmd = docker_cmd+"--prop:nsx_netmask_0='"+config.E2EP_ENVIRONMENT().subnet_mask+"' "
    docker_cmd = docker_cmd+"--prop:nsx_gateway_0='"+config.E2EP_ENVIRONMENT().default_gw+"' "
    docker_cmd = docker_cmd+"--prop:nsx_dns1_0='"+config.DNS().ip+"' "
    docker_cmd = docker_cmd+"--prop:nsx_ntp_0='"+config.E2EP_ENVIRONMENT().ntp_server+"' "
    docker_cmd = docker_cmd+"--prop:nsx_passwd_0='"+config.NSX().password+"' "
    docker_cmd = docker_cmd+"--prop:nsx_cli_passwd_0='"+config.NSX().password+"' "
    docker_cmd = docker_cmd+"--prop:nsx_cli_audit_passwd_0='"+config.NSX().password+"' "
    docker_cmd = docker_cmd+"--prop:nsx_isSSHEnabled=True "
    docker_cmd = docker_cmd+"--prop:nsx_allowSSHRootLogin=True "
    docker_cmd = docker_cmd+"'"+config.NSX().nsx_ova_source+"' "
    #docker_cmd = docker_cmd+"vi://'"+config.E2EP_ENVIRONMENT().esxi_host_username+"':'"+config.E2EP_ENVIRONMENT().esxi_host_password+"'@"+config.E2EP_ENVIRONMENT().esxi_host_ip
    docker_cmd = docker_cmd+"vi://'administrator@vsphere.local':'VMware1!'@172.16.0.10"
    dclient = docker.from_env()
    err = dclient.containers.run(image=docker_image, volumes=docker_volume, tty=True, working_dir="/root/home", remove=True, command=docker_cmd)
    return str(err)

def docker_build(path_to_Dockerfile):
    dclient = docker.from_env()
    err=dclient.images.build(path=path_to_Dockerfile)
    return err
