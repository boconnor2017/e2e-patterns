# Builds PhotonOS virtual appliance using ovftool container
# Author: Brendan O'Connor
# Date: August 2023
# Add python script (example below)
import os
import shutil
import subprocess
import sys

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
logfile_name = config.LOGS().photonos
err = "Starting wrapper-build-e2e-pattern-photon.py"
lib.write_to_logs(err, logfile_name)
err = "Input variables:"
lib.write_to_logs(err, logfile_name)
i=0 
for args in sys.argv:
	err = "    "+args[i]
	lib.write_to_logs(err, logfile_name)
	i=i+1

# Virtual Machine Details
class VM():
	name = sys.argv[1] # as displayed in vCenter
	hostname = sys.argv[2] # guest os config 
	ip = sys.argv[3] # guest os config
	source = sys.argv[4] # (syntax: ova-name.ova)

err = "Class VM():"
lib.write_to_logs(err, logfile_name)
err = "	   name: "+VM().name
lib.write_to_logs(err, logfile_name)
err = "	   hostname: "+VM().hostname
lib.write_to_logs(err, logfile_name)
err = "	   ip: "+VM().ip
lib.write_to_logs(err, logfile_name)
err = "	   source: "+VM().source
lib.write_to_logs(err, logfile_name)

# Build ovftool command with params - ESXi
def build_ovftool_cmd():
    ovftool_cmd = ["docker run -it --rm -v /usr/local/drop:/root/home -w /root/home ovftool "]
    ovftool_cmd.append("--sourceType=OVA ")
    ovftool_cmd.append("--acceptAllEulas ")
    ovftool_cmd.append("--allowExtraConfig ")
    ovftool_cmd.append("--noSSLVerify ")
    ovftool_cmd.append("--diskMode=thin ")
    ovftool_cmd.append("--powerOn ")
    ovftool_cmd.append("--datastore='"+config.E2EP_ENVIRONMENT().esxi_host_datastore+"' ")
    ovftool_cmd.append("--network='"+config.E2EP_ENVIRONMENT().esxi_host_virtual_switch+"' ")
    ovftool_cmd.append("--name='"+VM().name+"' ")
    ovftool_cmd.append("'"+VM().source+"' ")
    ovftool_cmd.append("vi://'"+config.E2EP_ENVIRONMENT().esxi_host_username+"':'"+config.E2EP_ENVIRONMENT().esxi_host_password+"'@"+config.E2EP_ENVIRONMENT().esxi_host_ip)
    return ovftool_cmd

# Write ovftool command to temporary bash file
def write_ovftool_cmd_to_temp_bash(ovftool_cmd, temp_bash_file_name):
    ovftool_sh_file = open(temp_bash_file_name, "w")
    ovftool_sh_file.writelines(ovftool_cmd)
    ovftool_sh_file.close()

# Create temporary bash file
err = ""
lib.write_to_logs(err, logfile_name)
temp_bash_file_path = "/usr/local/drop/"
temp_bash_file_name = temp_bash_file_path+"temp_ovftool_run_esxi.sh"
err = "temp_bash_file_name: "+temp_bash_file_name

# Build ovftool command 
ovftool_cmd = build_ovftool_cmd()
err = ""
lib.write_to_logs(err, logfile_name)
err = "ovftool_cmd:"
lib.write_to_logs(err, logfile_name)
i=0
for cmd in ovftool_cmd:
	err = "    "+ovftool_cmd[i]
	lib.write_to_logs(err, logfile_name)
	i=i+1
err = ""
lib.write_to_logs(err, logfile_name)

# Write ovftool command to temp bash file
write_ovftool_cmd_to_temp_bash(ovftool_cmd, temp_bash_file_name)
err = "Writing ovftool_cmd to "+temp_bash_file_name
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Build OVA 
print("Directory: "+os.getcwd())
os.chdir('/usr/local/drop')
print("Directory: "+os.getcwd())
subprocess.run(["sh", temp_bash_file_name])

