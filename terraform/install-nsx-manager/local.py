# Description: local.py for Pattern C-02
# Author: Brendan O'Connor
# Date: September 2023
# Version: 1.0

# Base imports
import os
import shutil
import sys

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

'''
local.py steps:
01. Build nsx.tfvars file
02. Run terraform init command (dir)
03. Run terraform apply command (dir)
'''

# Build nsx.tfvars file


# Run terraform init 
err = lib.run_terraform_init(des_dir)

# Run terraform apply
err = lib.run_terraform_apply(des_dir)
