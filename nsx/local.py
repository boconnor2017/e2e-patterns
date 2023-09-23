# local.py

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

# Copy main.tf to /usr/local/drop
src_file = config.NSX().nsx_terraform_source
des_dir = "/usr/local/drop"
outpt = shutil.copy(src_file, des_dir)

# Run terraform init 
err = lib.run_terraform_init(des_dir)

# Run terraform apply
err = lib.run_terraform_apply(des_dir)
