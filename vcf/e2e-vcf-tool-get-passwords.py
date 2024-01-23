# Description: Parses VCF JSON File for Passwords
# Author: Brendan O'Connor
# Date: January 2024
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
print("Passwords for Management Workload Domain:")
print("    SDDC Manager: "+vcf_json["sddcManagerSpec"]["rootUserCredentials"]["password"])
print("    Root NSX Manager Password: "+vcf_json["nsxtSpec"]["rootNsxtManagerPassword"])
print("    NSXT Admin Password: "+vcf_json["nsxtSpec"]["nsxtAdminPassword"])
print("    NSXT Audit Password: "+vcf_json["nsxtSpec"]["nsxtAuditPassword"])
print("    vCenter: "+vcf_json["vcenterSpec"]["rootVcenterPassword"])
print("    ESXi Host 01: "+vcf_json["hostSpecs"][0]["credentials"]["password"])
print("    ESXi Host 02: "+vcf_json["hostSpecs"][1]["credentials"]["password"])
print("    ESXi Host 03: "+vcf_json["hostSpecs"][2]["credentials"]["password"])
print("    ESXi Host 04: "+vcf_json["hostSpecs"][3]["credentials"]["password"])
