# Description: Create VCF 5 var file for Terraform
# Author: Brendan O'Connor
# Date: November 2023
# Version: 1.0

# Base imports
import os
import shutil
import sys
import json
from os.path import exists

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

# Scrape VCF JSON file
vcf_json_file_name = os.getcwd()+"/vcf.json"
vcf_json_raw = lib.populate_var_from_file(vcf_json_file_name)
vcf_json = json.loads(vcf_json_raw)

# Build vcf_vars.tf file
tf_var_txt = ["# vcf.tfvars file",
"variable \"cloud_builder_username\" { default = \"admin\" }" ,
"variable \"cloud_builder_password\" { default = \""+config.CLOUD_BUILDER().password+"\" }",
"variable \"cloud_builder_host\" { default = \""+config.CLOUD_BUILDER().ip+"\" }",
"variable \"sddc_manager_root_user_password\" {default = \""+vcf_json["sddcManagerSpec"]["rootUserCredentials"]["password"]+"\"}",
"variable \"sddc_manager_secondary_user_password\" {default = \""+vcf_json["sddcManagerSpec"]["localUserPassword"]+"\"}",
"variable \"vcenter_root_password\" { default = \""+vcf_json["vcenterSpec"]["rootVcenterPassword"]+"\"}",
"variable \"nsx_manager_admin_password\" { default = \""+vcf_json["nsxtSpec"]["nsxtAdminPassword"]+"\"}",
"variable \"nsx_manager_audit_password\" { default = \""+vcf_json["nsxtSpec"]["nsxtAuditPassword"]+"\" }",
"variable \"nsx_manager_root_password\" { default = \""+vcf_json["nsxtSpec"]["rootNsxtManagerPassword"]+"\" }",
"variable \"esx_host1_pass\" { default = \"/usr/local/drop/"+vcf_json["hostSpecs"][0]["credentials"]["password"]+"\" }",
"variable \"esx_host2_pass\" { default = \"/usr/local/drop/"+vcf_json["hostSpecs"][1]["credentials"]["password"]+"\" }",
"variable \"esx_host3_pass\" { default = \"/usr/local/drop/"+vcf_json["hostSpecs"][2]["credentials"]["password"]+"\" }",
"variable \"esx_host4_pass\" { default = \"/usr/local/drop/"+vcf_json["hostSpecs"][3]["credentials"]["password"]+"\" }",
"variable \"nsx_license_key\" { default = \""+vcf_json["nsxtSpec"]["nsxtLicense"]+"\" }",
"variable \"nsx_license_key\" { default = \""+vcf_json["nsxtSpec"]["nsxtLicense"]+"\" }",
"variable \"vcenter_license_key\" { default = \""+vcf_json["vcenterSpec"]["licenseFile"]+"\" }",
"variable \"vsan_license_key\" { default = \""+vcf_json["vsanSpec"]["licenseFile"]+"\" }",
"variable \"esx_license_key\" { default = \""+vcf_json["esxLicense"]
]

tf_var_file_name = "vcf_var.tf"
tf_var_file_exists = exists(tf_var_file_name)
if tf_var_file_exists:
    os.remove(tf_var_file_name)

for line in tf_var_txt:
    lib.append_text_to_file(line+"\n", tf_var_file_name)

