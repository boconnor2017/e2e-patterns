# Description: Parses VCF JSON File for DNS Entries
# Author: Brendan O'Connor
# Date: January 2024
# Version: 2.0

# lib and config filenames for the year 
# Must be available in /e2e-patterns repository
lib_filename = "lib2024.py"
config_filename = "config2024.py"

# Base imports
import os
import shutil
import json 

# Copy latest lib and config files
fullpath = os.getcwd()
dirs = fullpath.split('/')
count_dirs = len(dirs)
currdir = dirs[count_dirs-1]
homedir = dirs[count_dirs-2]
shell_dir = ""
i=0 
for x in dirs:
    if i == 0:
        shell_dir = "/"
        i=i+1
    if i == (count_dirs-1):
        shell_dir = shell_dir
    if i == (count_dirs-2):
        shell_dir = shell_dir
    else:
        shell_dir = shell_dir+dirs[i]+"/"
        i=i+1

lib_path = shell_dir+homedir+"/"+lib_filename
config_path = shell_dir+homedir+"/"+config_filename
shutil.copy(lib_path, fullpath)
os.rename(lib_filename, "lib.py")
shutil.copy(config_path, fullpath)
os.rename(config_filename, "config.py")

# Import pattern config and library
import config
import lib

# Parse JSON for DNS Entries
vcf_json_file_name = os.getcwd()+"/vcf.json"
vcf_json_raw = lib.populate_var_from_file(vcf_json_file_name)
vcf_json = json.loads(vcf_json_raw)
print("DNS Entries for Management Workload Domain:")
print("    DNS Servers: "+vcf_json["dnsSpec"]["nameserver"]+", "+vcf_json["dnsSpec"]["secondaryNameserver"])
print("    DNS Zone: "+vcf_json["dnsSpec"]["domain"])
print("    SDDC Manager: "+vcf_json["sddcManagerSpec"]["hostname"]+" "+vcf_json["sddcManagerSpec"]["ipAddress"]+" (Subnet Mask: "+vcf_json["sddcManagerSpec"]["netmask"]+")")
print("    NSX Manager 01: "+vcf_json["nsxtSpec"]["nsxtManagers"][0]["hostname"]+" "+vcf_json["nsxtSpec"]["nsxtManagers"][0]["ip"])
print("    NSX Manager 02: "+vcf_json["nsxtSpec"]["nsxtManagers"][1]["hostname"]+" "+vcf_json["nsxtSpec"]["nsxtManagers"][1]["ip"])
print("    NSX Manager 03: "+vcf_json["nsxtSpec"]["nsxtManagers"][2]["hostname"]+" "+vcf_json["nsxtSpec"]["nsxtManagers"][2]["ip"])
print("    NSX Manager VIP: "+vcf_json["nsxtSpec"]["vipFqdn"]+" "+vcf_json["nsxtSpec"]["vip"])
print("    vCenter: "+vcf_json["vcenterSpec"]["vcenterHostname"]+" "+vcf_json["vcenterSpec"]["vcenterIp"])
print("    ESXi Host 01: "+vcf_json["hostSpecs"][0]["hostname"]+" "+vcf_json["hostSpecs"][0]["ipAddressPrivate"]["ipAddress"]+" (Gateway: "+vcf_json["hostSpecs"][0]["ipAddressPrivate"]["gateway"]+", Subnet Mask: "+vcf_json["hostSpecs"][0]["ipAddressPrivate"]["subnet"]+")")
print("    ESXi Host 02: "+vcf_json["hostSpecs"][1]["hostname"]+" "+vcf_json["hostSpecs"][1]["ipAddressPrivate"]["ipAddress"]+" (Gateway: "+vcf_json["hostSpecs"][1]["ipAddressPrivate"]["gateway"]+", Subnet Mask: "+vcf_json["hostSpecs"][1]["ipAddressPrivate"]["subnet"]+")")
print("    ESXi Host 03: "+vcf_json["hostSpecs"][2]["hostname"]+" "+vcf_json["hostSpecs"][2]["ipAddressPrivate"]["ipAddress"]+" (Gateway: "+vcf_json["hostSpecs"][2]["ipAddressPrivate"]["gateway"]+", Subnet Mask: "+vcf_json["hostSpecs"][2]["ipAddressPrivate"]["subnet"]+")")
print("    ESXi Host 04: "+vcf_json["hostSpecs"][3]["hostname"]+" "+vcf_json["hostSpecs"][3]["ipAddressPrivate"]["ipAddress"]+" (Gateway: "+vcf_json["hostSpecs"][3]["ipAddressPrivate"]["gateway"]+", Subnet Mask: "+vcf_json["hostSpecs"][3]["ipAddressPrivate"]["subnet"]+")")
