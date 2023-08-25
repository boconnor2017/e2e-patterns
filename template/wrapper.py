# Wrapper files should follow this naming convention: wrapper-build-e2e-pattern-<NAME>.py
# Copy Template Below
# # # # # # # # # # # # # # # # # # # # # # # # #
# <DESCRIPTION>
# Author: Brendan O'Connor
# Date: <MONTH YEAR>
# Add python script (example below)
a = "This works!!"
print(a)

# Get pattern config file
src_file = '/usr/local/e2e-patterns/config.py'
des_dir = os.getcwd()
print("Retrieving config file from "+src_file+" and copying to "+des_dir)
outpt = shutil.copy(src_file, des_dir)
print(str(outpt))
print("")

# Get pattern library
src_file = '/usr/local/e2e-k8-lab/lib.py'
des_dir = os.getcwd()
print("Retrieving library file from "+src_file+" and copying to "+des_dir)
outpt = shutil.copy(src_file, des_dir)
print(str(outpt))
print("")

import config
import lib
