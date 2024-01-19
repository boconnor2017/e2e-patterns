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

def api_get(api_url):
    api_response = requests.get(api_url)
    return api_response

def api_post(api_url):
    api_response = requests.post(api_url)
    api_response.headers['Content-Type: application/json']
    return api_response

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

def docker_powercli_attach_iso_to_vm(vm_name, datastore, filepath, iso):
    download_file_from_github(config.SCRIPTS().attach_iso_to_vm_with_powercli_url, config.SCRIPTS().attach_iso_to_vm_with_powercli_filename) 
    docker_rm = True
    docker_entrypoint = "/usr/bin/pwsh"
    docker_volume = {os.getcwd():{'bind':'/tmp', 'mode':'rw'}}
    docker_image = "vmware/powerclicore"
    docker_cmd = "/tmp/"+config.SCRIPTS().attach_iso_to_vm_with_powercli_filename+" \""
    docker_cmd = docker_cmd+config.E2EP_ENVIRONMENT().esxi_host_ip+" "
    docker_cmd = docker_cmd+config.E2EP_ENVIRONMENT().esxi_host_username+" "
    docker_cmd = docker_cmd+config.E2EP_ENVIRONMENT().esxi_host_password+" "
    docker_cmd = docker_cmd+vm_name+" "
    docker_cmd = docker_cmd+datastore+" "
    docker_cmd = docker_cmd+filepath+iso
    docker_cmd = docker_cmd+"\""
    dclient = docker.from_env()
    err = dclient.containers.run(image=docker_image, entrypoint=docker_entrypoint, volumes=docker_volume, remove=docker_rm, command=docker_cmd)
    return err

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
    err = dclient.containers.run(image=docker_image, entrypoint=docker_entrypoint, volumes=docker_volume, remove=docker_rm, command=docker_cmd)
    return err

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

def docker_powercli_get_vm_list():
    download_file_from_github(config.SCRIPTS().get_vm_list_with_powercli_url, config.SCRIPTS().get_vm_list_with_powercli_filename) 
    docker_rm = True
    docker_entrypoint = "/usr/bin/pwsh"
    docker_volume = {os.getcwd():{'bind':'/tmp', 'mode':'rw'}}
    docker_image = "vmware/powerclicore"
    docker_cmd = "/tmp/"+config.SCRIPTS().get_vm_list_with_powercli_filename+" \""+config.E2EP_ENVIRONMENT().esxi_host_ip+" "+config.E2EP_ENVIRONMENT().esxi_host_username+" "+config.E2EP_ENVIRONMENT().esxi_host_password+"\""
    dclient = docker.from_env()
    vm_list_raw = dclient.containers.run(image=docker_image, entrypoint=docker_entrypoint, volumes=docker_volume, remove=docker_rm, command=docker_cmd)
    vm_list_raw = str(vm_list_raw)
    vm_list = vm_list_raw.split('\\n')
    vm_list_summarized = ""
    i=0 
    for x in vm_list:
        if i == 14:
            vm_list_summarized = x
            i=i+1
        else: 
            i=i+1
    vm_list = []
    i=0
    vm_list_raw = vm_list_summarized.split('@')
    for x in vm_list_raw:
        x = x.replace("{Name=", "")
        x = x.replace("}", "")
        x = x.replace(" ", "")
        if i == 0:
            i=i+1
        else:
            vm_list.append(x)
            i=i+1
    return vm_list

def e2e_build_node_controller(vm_name, logfile_name):
    err = "Starting e2e_build_node_controller:"
    write_to_logs(err, logfile_name)
    err = "    VM Name: "+vm_name
    write_to_logs(err, logfile_name)
    err = ""
    write_to_logs(err, logfile_name)
    err = "Step 1: docker_ovftool_deploy_photon"
    write_to_logs(err, logfile_name)
    err = docker_ovftool_deploy_photon(vm_name)
    write_to_logs(err, logfile_name)
    err = ""
    write_to_logs(err, logfile_name)
    seconds = (60*2)
    write_to_logs(err, logfile_name)
    err = "Pausing for "+str(seconds)+" seconds to let the ova to complete its build."
    write_to_logs(err, logfile_name)
    pause_python_for_duration(seconds)
    err = "Resuming build."
    write_to_logs(err, logfile_name)
    err = ""
    write_to_logs(err, logfile_name)
    err = "Step 2: docker_powercli_change_default_photonos_password()"
    write_to_logs(err, logfile_name)
    err = docker_powercli_change_default_photonos_password(vm_name, config.PHOTONOS().password)
    err = str(err)
    write_to_logs(err, logfile_name)
    err = ""
    write_to_logs(err, logfile_name)
    err = "Step 3: docker_powercli_get_vm_ip_address"
    write_to_logs(err, logfile_name)
    ip_address = docker_powercli_get_vm_ip_address(vm_name)
    err = "    IP Address of "+vm_name+": "+ip_address
    write_to_logs(err, logfile_name)
    err = ""
    write_to_logs(err, logfile_name)
    seconds = (60*1)
    write_to_logs(err, logfile_name)
    err = "Pausing for "+str(seconds)+" seconds to let the password change to take effect."
    write_to_logs(err, logfile_name)
    pause_python_for_duration(seconds)
    err = "Resuming build."
    write_to_logs(err, logfile_name)
    err = ""
    write_to_logs(err, logfile_name)
    err = "Step 4: paramiko_download_file_to_remote_photon_vm()"
    write_to_logs(err, logfile_name)
    err = "    File #1: "+config.SCRIPTS().refresh_e2e_patterns_filename
    write_to_logs(err, logfile_name)
    paramiko_download_file_to_remote_photon_vm(ip_address, config.PHOTONOS().username, config.PHOTONOS().password, config.SCRIPTS().refresh_e2e_patterns_url, '/usr/local/', config.SCRIPTS().refresh_e2e_patterns_filename)
    err = "    File #2: "+config.SCRIPTS().photon_prep_script_filename
    write_to_logs(err, logfile_name)
    paramiko_download_file_to_remote_photon_vm(ip_address, config.PHOTONOS().username, config.PHOTONOS().password, config.SCRIPTS().photon_prep_script_url, '/usr/local/', config.SCRIPTS().photon_prep_script_filename)
    err = ""
    write_to_logs(err, logfile_name)
    seconds = (60*1)
    write_to_logs(err, logfile_name)
    err = "Pausing for "+str(seconds)+" seconds to let the prep scripts to download from github."
    write_to_logs(err, logfile_name)
    pause_python_for_duration(seconds)
    err = "Resuming build."
    write_to_logs(err, logfile_name)
    err = ""
    write_to_logs(err, logfile_name)
    err = "Step 5: paramiko_run_sh_on_remote_photon_vm()"
    write_to_logs(err, logfile_name)
    err = "    Script: "+config.SCRIPTS().photon_prep_script_filename
    write_to_logs(err, logfile_name)
    paramiko_run_sh_on_remote_photon_vm(ip_address, config.PHOTONOS().username, config.PHOTONOS().password, '/usr/local/', config.SCRIPTS().photon_prep_script_filename)
    err = ""
    write_to_logs(err, logfile_name)
    err = "e2e_build_node_controller is finished. "
    write_to_logs(err, logfile_name)

def e2e_check_for_node_controller(vm_name):
    vm_list = docker_powercli_get_vm_list()
    node_controller_exists = 0
    for x in vm_list:
        if x == vm_name:
            node_controller_exists = node_controller_exists+1
        else:
            node_controller_exists = node_controller_exists+0
    return node_controller_exists

def e2e_create_datacenter_in_vcenter(vcenter_session_id, vcenter_hostname, datacenter_name):
    api_call = requests.post("https://"+vcenter_hostname+"/api/vcenter/datacenter", verify=False, headers={
    "vmware-api-session-id": vcenter_session_id
    }, json={
    "folder": "group-d1",
    "name": datacenter_name
    })
    datacenter = api_call.json()
    return datacenter

def e2e_get_vcenter_session_id(vcenter_hostname, vcenter_username, vcenter_password):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    sess = requests.post("https://"+vcenter_hostname+"/rest/com/vmware/cis/session", auth=(vcenter_username, vcenter_password), verify=False)
    session_id = sess.json()['value']
    return(session_id)

def e2e_install_vCenter_using_node_controller(nc_ip_address, logfile_name):
    err = "Starting e2e_install_vCenter_using_node_controller()."
    write_to_logs(err, logfile_name)
    run_vcsa_installer_cmd = "sh /usr/local/mount/vcsa-cli-installer/lin64/./vcsa-deploy "
    run_vcsa_installer_cmd = run_vcsa_installer_cmd+"install "+config.VCSA().json_filepath+config.VCSA().json_filename+" "
    run_vcsa_installer_cmd = run_vcsa_installer_cmd+"--accept-eula --acknowledge-ceip --no-ssl-certificate-verification "
    run_vcsa_installer_cmd = run_vcsa_installer_cmd+">> /usr/local/e2e-patterns/vcsa/_vcsa-deploy.log"
    err = "run_vcsa_installer_cmd:"
    write_to_logs(err, logfile_name)
    err = ""
    write_to_logs(err, logfile_name)
    err = "- - - - - - - - - - - - - - - - - - - - - - -"
    write_to_logs(err, logfile_name)
    err = run_vcsa_installer_cmd
    write_to_logs(err, logfile_name)
    err = ""
    write_to_logs(err, logfile_name)
    err = "- - - - - - - - - - - - - - - - - - - - - - -"
    write_to_logs(err, logfile_name)
    err = ""
    write_to_logs(err, logfile_name)
    stdout = paramiko_send_command_over_ssh(run_vcsa_installer_cmd, nc_ip_address, config.PHOTONOS().username, config.PHOTONOS().password)
    seconds = (35*60)
    err = "Pausing for "+str(seconds)+" seconds ("+str(seconds/60)+" minutes) to allow vcenter to complete its build process."
    write_to_logs(err, logfile_name)
    err = "vcenter deploy log can be found on the node controller at /usr/local/e2e-patterns/vcsa/_vcsa-deploy.log"
    write_to_logs(err, logfile_name)
    pause_python_for_duration(seconds)
    err = str(seconds)+" pause has completed. Resuming script."
    write_to_logs(err, logfile_name)    

def paramiko_download_file_to_remote_photon_vm(ip, un, pw, url, filepath, filename):
    # filepath format: /foo/bar/
    # filename format: somefile.xyz
    cmd = "curl "+url+" >> "+filepath+filename
    paramiko_send_command_over_ssh(cmd, ip, un, pw)

def paramiko_run_sh_on_remote_photon_vm(ip, un, pw, entrypoint, shscript):
    # entrypoint format: /foo/bar/
    # shscript format: shfile.sh
    cmd = "sh "+entrypoint+shscript
    paramiko_send_command_over_ssh(cmd, ip, un, pw)

def paramiko_move_file_to_remote_photon_vm(ip, un, pw, file_as_var, filepath, filename):
    # file_as_var: read contents of file into a variable
    # filepath format: /foo/bar/
    # filename format: somefile.xyz
    cmd = "echo \'"+file_as_var+"\' >> "+filepath+filename
    paramiko_send_command_over_ssh(cmd, ip, un, pw)

def paramiko_send_command_over_ssh(cmd, ip, un, pw):
    pclient = paramiko.SSHClient()
    pclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    pclient.connect(hostname=ip, username=un, password=pw)
    stdin, stdout, stderr = pclient.exec_command(cmd, timeout=None)
    stdout=stdout.readlines()
    pclient.close()
    return stdout

def pause_python_for_duration(seconds):
    time.sleep(seconds)

def run_local_shell_cmd(cmd):
    err = subprocess.run(cmd, capture_output=True)
    return err

def tanium_get_token(username, password):
    api_url = "http://"+config.DNS().ip+":"+config.DNS().port+"/api/user/login?user="+username+"&pass="+password+"&includeInfo=true"
    api_response = api_get(api_url)
    tanium_token = (api_response.json()['token'])
    return tanium_token

def tanium_change_password(tanium_token, new_password):
    api_url = "http://"+config.DNS().ip+":"+config.DNS().port+"/api/user/changePassword?token="+tanium_token+"&pass="+new_password
    api_response = api_get(api_url)
    return api_response

def tanium_create_dns_record(tanium_token, domain_name, dns_zone, ip_address):
    api_url = "http://"+config.DNS().ip+":"+config.DNS().port+"/api/zones/records/add?"
    api_url = api_url+"token="+tanium_token
    api_url = api_url+"&domain="+domain_name+"."+dns_zone
    api_url = api_url+"&zone="+dns_zone
    api_url = api_url+"&type=A"
    api_url = api_url+"&ttl=3600"
    api_url = api_url+"&overwrite=true"
    api_url = api_url+"&ipAddress="+ip_address
    api_url = api_url+"&ptr=true"
    api_url = api_url+"&createPtrZone=true"
    api_response = api_get(api_url)
    return api_response 

def tanium_create_dns_zone(tanium_token, dns_zone):
    api_url = "http://"+config.DNS().ip+":"+config.DNS().port+"/api/zones/create?token="+tanium_token+"&zone="+dns_zone+"&type=Primary"
    api_response = api_get(api_url)
    return api_response

def write_to_logs(err, logfile_name):
    tstamp = str(datetime.now())
    logfile = open(logfile_name, "a")
    logfile.write(tstamp+": "+err+" \n")
    logfile.close
