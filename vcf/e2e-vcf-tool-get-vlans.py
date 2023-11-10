# Description: Parses VCF JSON File for VLANs
# Author: Brendan O'Connor
# Date: November 2023
# Version: 1.0

# Base imports
import os
import shutil
import sys
import json

# Get pattern config file and library
des_dir = str(os.getcwd())
os.chdir("../")
src_dir = str(os.getcwd())
os.chdir(des_dir)
src_file = src_dir+'/config.py'
outpt = shutil.copy(src_file, des_dir)
src_file = src_dir+'/lib.py'
outpt = shutil.copy(src_file, des_dir)

# Import pattern config and library
import config
import lib

vcf_json_file_name = os.getcwd()+"/vcf.json"
vcf_json_raw = lib.populate_var_from_file(vcf_json_file_name)
vcf_json = json.loads(vcf_json_raw)
print("VLANs:")
print("    "+vcf_json["networkSpecs"][0]["networkType"])
print("        VLAN ID: "+vcf_json["networkSpecs"][0]["vlanId"])
print("        MTU: "+vcf_json["networkSpecs"][0]["mtu"])
print("        Gateway: "+vcf_json["networkSpecs"][0]["gateway"])
print("    "+vcf_json["networkSpecs"][1]["networkType"])
print("        VLAN ID: "+vcf_json["networkSpecs"][1]["vlanId"])
print("        MTU: "+vcf_json["networkSpecs"][1]["mtu"])
print("        Gateway: "+vcf_json["networkSpecs"][1]["gateway"])
print("    "+vcf_json["networkSpecs"][2]["networkType"])
print("        VLAN ID: "+vcf_json["networkSpecs"][2]["vlanId"])
print("        MTU: "+vcf_json["networkSpecs"][2]["mtu"])
print("        Gateway: "+vcf_json["networkSpecs"][2]["gateway"])
print("    TEP")
print("        Transport VLAN ID: "+str(vcf_json["nsxtSpec"]["transportVlanId"]))
print("        CIDR: "+vcf_json["nsxtSpec"]["ipAddressPoolSpec"]["subnets"][0]["cidr"])
print("        Gateway: "+vcf_json["nsxtSpec"]["ipAddressPoolSpec"]["subnets"][0]["gateway"])
