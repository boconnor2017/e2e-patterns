# Description: Parses VCF JSON File and Create TF Var File
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
from os.path import exists

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
