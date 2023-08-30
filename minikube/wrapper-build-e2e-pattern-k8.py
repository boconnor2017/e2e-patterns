# Deploys a Minikube Pattern
# Author: Brendan O'Connor
# Date: August 2023
# Add python script (example below)
import os
import shutil

# Get pattern config file
src_file = '/usr/local/e2e-patterns/config.py'
des_dir = os.getcwd()
print("Retrieving config file from "+src_file+" and copying to "+des_dir)
outpt = shutil.copy(src_file, des_dir)
print(str(outpt))
print("")

# Get pattern library
src_file = '/usr/local/e2e-patterns/lib.py'
des_dir = os.getcwd()
print("Retrieving library file from "+src_file+" and copying to "+des_dir)
outpt = shutil.copy(src_file, des_dir)
print(str(outpt))
print("")

import config
import lib

#TEST 
a = "This works!!"
b = config.IPAM().tag[0] 
c = config.IPAM().fqdn[0]
d = config.IPAM().ip[0]
e = a 
f = "_log_test.log"

print(a)
print(b+" "+c+" "+d)
lib.write_to_logs(e, f)
