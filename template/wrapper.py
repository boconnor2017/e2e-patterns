# Wrapper files should follow this naming convention: wrapper-build-e2e-pattern-<NAME>.py
# Copy Template Below
# # # # # # # # # # # # # # # # # # # # # # # # #
# <DESCRIPTION>
# Author: Brendan O'Connor
# Date: <MONTH YEAR>
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

# Start log file
logfile_name = config.LOGS().template
err = "Starting wrapper-build-e2e-pattern-photon.py"
lib.write_to_logs(err, logfile_name)
err = "Input variables:"
lib.write_to_logs(err, logfile_name)
i=0 
for args in sys.argv:
	err = "    "+args[i]
	lib.write_to_logs(err, logfile_name)
	i=i+1


#TEST 
a = "This works!!"
b = config.IPAM().tag[0] 
c = config.IPAM().fqdn[0]
d = config.IPAM().ip[0]
e = a 


print(a)
print(b+" "+c+" "+d)

