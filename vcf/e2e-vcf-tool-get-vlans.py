# Description: Parses VCF JSON File for VLANs
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

# Parse JSON for VLANs
vcf_json_file_name = os.getcwd()+"/vcf.json"
vcf_json_raw = lib.populate_var_from_file(vcf_json_file_name)
vcf_json = json.loads(vcf_json_raw)
print("VLANs:")
print("    "+vcf_json["networkSpecs"][0]["networkType"])
print("        Subnet: "+vcf_json["networkSpecs"][0]["subnet"])
print("        VLAN ID: "+vcf_json["networkSpecs"][0]["vlanId"])
print("        MTU: "+vcf_json["networkSpecs"][0]["mtu"])
print("        Gateway: "+vcf_json["networkSpecs"][0]["gateway"])
print("    "+vcf_json["networkSpecs"][1]["networkType"])
print("        Subnet: "+vcf_json["networkSpecs"][1]["subnet"])
print("        VLAN ID: "+vcf_json["networkSpecs"][1]["vlanId"])
print("        MTU: "+vcf_json["networkSpecs"][1]["mtu"])
print("        Gateway: "+vcf_json["networkSpecs"][1]["gateway"])
print("    "+vcf_json["networkSpecs"][2]["networkType"])
print("        Subnet: "+vcf_json["networkSpecs"][2]["subnet"])
print("        VLAN ID: "+vcf_json["networkSpecs"][2]["vlanId"])
print("        MTU: "+vcf_json["networkSpecs"][2]["mtu"])
print("        Gateway: "+vcf_json["networkSpecs"][2]["gateway"])
print("    TEP")
print("        Transport VLAN ID: "+str(vcf_json["nsxtSpec"]["transportVlanId"]))
print("        CIDR: "+vcf_json["nsxtSpec"]["ipAddressPoolSpec"]["subnets"][0]["cidr"])
print("        Gateway: "+vcf_json["nsxtSpec"]["ipAddressPoolSpec"]["subnets"][0]["gateway"])
