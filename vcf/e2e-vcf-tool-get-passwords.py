# Description: Parses VCF JSON File for Passwords
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

# Parse JSON for Passwords
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
