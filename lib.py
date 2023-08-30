# Python Library for the E2E Patterns Lab
# Author: Brendan O'Connor
# Date: August 2023 (Version 2.0)

import requests
import urllib3
import urllib
import shutil
import time
import json
import os
from vmware.vapi.vsphere.client import create_vsphere_client
from datetime import datetime
import config

## LOGGING
def write_to_logs(err, logfile_name):
    tstamp = str(datetime.now())
    logfile = open(logfile_name, "a")
    logfile.write(tstamp+": "+err+" \n")
    logfile.close

## GENERIC
def pause_python_for_duration(seconds):
    time.sleep(seconds)

def build_script_file(script, scriptfile_name):
	scriptfile = open(scriptfile_name, "w")
	scriptfile.writelines(script)
	scriptfile.close

def check_web_service_status(web_svc_url):
    return_code = urllib.request.urlopen(web_svc_url).getcode()
    return return_code

def get_vm_name_from_hostname(hostname):
    vm_name = hostname.replace("."+labvars.dns_server_zone, "")
    return(vm_name)

## DNS
def create_dns_record(e2e_tag, e2e_fqdn, e2e_ip, token):
  api_domain = e2e_fqdn
  api_type = "A"
  api_ttl = "3600"
  api_ptr = "true"
  api_createPtrZone = "true"
  api_url = "http://localhost:5380/api/zone/addRecord?token="+token
  api_url = api_url+"&domain="+api_domain
  api_url = api_url+"&zone="+labvars.dns_server_zone
  api_url = api_url+"&type="+api_type
  api_url = api_url+"&ttl="+api_ttl
  api_url = api_url+"&ipAddress="+e2e_ip
  api_url = api_url+"&ptr="+api_ptr
  api_url = api_url+"&createPtrZone="+api_createPtrZone
  response = requests.get(api_url)
  return response.json()


## VAPI: GET CALLS
def get_vc_session_id(vcenter_hostname, vcenter_username, vcenter_password):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    sess = requests.post("https://"+vcenter_hostname+"/rest/com/vmware/cis/session", auth=(vcenter_username, vcenter_password), verify=False)
    session_id = sess.json()['value']
    return(session_id)

def get_vc_vm_list(session_id, vcenter_hostname):
    api_call = requests.get("https://"+vcenter_hostname+"/api/vcenter/vm", verify=False, headers={
   "vmware-api-session-id": session_id
    })
    return(api_call)

def get_vc_folders(session_id, vcenter_hostname):
    api_call = requests.get("https://"+vcenter_hostname+"/api/vcenter/folder", verify=False, headers={
   "vmware-api-session-id": session_id
   })
    return(api_call)

def get_vc_clusters(session_id, vcenter_hostname):
    api_call = requests.get("https://"+vcenter_hostname+"/api/vcenter/cluster", verify=False, headers={
   "vmware-api-session-id": session_id
   })
    return(api_call)

def get_vc_datacenters(session_id, vcenter_hostname):
    api_call = requests.get("https://"+vcenter_hostname+"/api/vcenter/datacenter", verify=False, headers={
   "vmware-api-session-id": session_id
   })
    return(api_call)

def get_vc_datastores(session_id, vcenter_hostname):
    api_call = requests.get("https://"+vcenter_hostname+"/api/vcenter/datastore", verify=False, headers={
   "vmware-api-session-id": session_id
   })
    return(api_call)

def get_vc_deployments(session_id, vcenter_hostname):
    api_call = requests.get("https://"+vcenter_hostname+"/api/vcenter/deployment", verify=False, headers={
   "vmware-api-session-id": session_id
   })
    return(api_call)

def get_vc_hosts(session_id, vcenter_hostname):
    api_call = requests.get("https://"+vcenter_hostname+"/api/vcenter/host", verify=False, headers={
   "vmware-api-session-id": session_id
   })
    return(api_call)

def get_vc_networks(session_id, vcenter_hostname):
    api_call = requests.get("https://"+vcenter_hostname+"/api/vcenter/network", verify=False, headers={
   "vmware-api-session-id": session_id
   })
    return(api_call)

def get_vc_resource_pools(session_id, vcenter_hostname):
    api_call = requests.get("https://"+vcenter_hostname+"/api/vcenter/resource-pool", verify=False, headers={
   "vmware-api-session-id": session_id
   })
    return(api_call)

def print_vc_object_list(list_as_json, object_type):
    print("Listing JSON for object type: "+object_type)
    for i in list_as_json:
        print(json.dumps(i))

## VAPI: POST CALLS
def post_vc_create_datacenter(session_id, vcenter_hostname, datacenter_name):
    folder_id = "group-d1" #todo: pull from API
    api_call = requests.post("https://"+vcenter_hostname+"/api/vcenter/datacenter", verify=False, headers={
   "vmware-api-session-id": session_id
   }, json={
   "folder": folder_id,
   "name": datacenter_name
    })
    datacenter = api_call.json()
    return datacenter

# PYVMOMI SDK Calls
def pyvmomi_setup():
    # Prerequisites for using PYVMOMI SDK
    # 01: pip updates
    os.system("python3 -m ensurepip")
    os.system("python3 -m pip install --upgrade pip")
    os.system("python3 -m pip install --upgrade pip setuptools")
    # 02: install pyvmomi lib
    os.system("python3 -m pip install pyvmomi")
    # 03: pull samples from github
    os.system("git clone https://github.com/vmware/pyvmomi-community-samples.git")
    # 04: run pyvmomi installation
    os.system("python3 pyvmomi-community-samples/setup.py install")

def pyvmomi_vc_create_vm(vcenter_hostname, vcenter_username, vcenter_password, vm_name, datacenter_name, datastore_name, host_ip):
    api_call = os.system("python3 pyvmomi-community-samples/samples/create_vm.py -s "+vcenter_hostname+" -o 443 -u "+vcenter_username+" -p "+vcenter_password+" -nossl -v "+vm_name+" --datacenter-name \""+datacenter_name+"\" --datastore-name "+datastore_name+" --esx-ip \""+host_ip+"\"")
    return(api_call)

def pyvmomi_vc_deploy_ova(vcenter_hostname, vcenter_username, vcenter_password, ova_path, datacenter_name, datastore_name):
    sdk_call = "python3 pyvmomi-community-samples/samples/deploy_ova.py -s "+vcenter_hostname+" -o 443 -u "+vcenter_username+" -p "+vcenter_password+" -nossl --ova-path "+ova_path+" --datacenter-name \""+datacenter_name+"\" --datastore-name "+datastore_name 
    os.system(sdk_call)
    return(sdk_call)

def pyvmomi_vc_rename_vm(vcenter_hostname, vcenter_username, vcenter_password, original_vm_name, new_vm_name):
     sdk_call = "python3 pyvmomi-community-samples/samples/renamer.py -s "+vcenter_hostname+" -o 443 -u "+vcenter_username+" -p "+vcenter_password+" -nossl -n \""+original_vm_name+"\" -r "+new_vm_name
     os.system(sdk_call)
     return(sdk_call)

def pyvmomi_vc_poweron_vm(vcenter_hostname, vcenter_username, vcenter_password, vm_name):
    sdk_call = "python3 pyvmomi-community-samples/samples/vm_power_on.py -s "+vcenter_hostname+" -o 443 -u "+vcenter_username+" -p "+vcenter_password+" -nossl -v "+vm_name
    os.system(sdk_call)
    return(sdk_call)
