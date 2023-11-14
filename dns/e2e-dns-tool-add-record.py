# Description: Creates DNS record in existing Tanium server
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


token = lib.get_dns_token()
domain_name = sys.argv[1]
ip = sys.argv[2]
create_dns_record(token, domain_name, config.DNS().zone, ip)
