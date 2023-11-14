# Description: Parses VCF JSON File for DNS Entries
# Author: Brendan O'Connor
# Date: November 2023
# Version: 1.1

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
