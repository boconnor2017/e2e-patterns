# Description: Builds Tanium DNS Server on a Node Controller
# Author: Brendan O'Connor
# Date: January 2024
# Version: 3.0

# lib and config filenames for the year 
# Must be available in /e2e-patterns repository
lib_filename = "lib2024.py"
config_filename = "config2024.py"

# Base imports
import os
import shutil

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

# Start log file
logfile_name = config.LOGS().dns
pattern_name = config.DNS().pattern
lib.e2e_patterns_header(logfile_name, pattern_name)
err = ""
lib.write_to_logs(err, logfile_name)

'''
01. Build Node Controller
02. Change IP Address of Node Controller to config.DNS().ip
03. Configure Tanium Prerequisites  
    a. Run configure-tanium-ip-tables.sh script
    b. Run run-docker-compose.sh script 

04. Install Tanium
05. Change Default Password
    a. Get Token using admin/admin 
    b. Change password 
    c. Get Token using permanent password 
'''

# 01. Build Node Controller
err = "01. Build Node Controller Started."
lib.write_to_logs(err, logfile_name)
lib.e2e_build_node_controller(vm_name, logfile_name)
err = "01. Build Node Controller Finished."
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# 02. Change IP Address of Node Controller to config.DNS().ip
err = "02. Change IP Address of Node Controller to config.DNS().ip Started."
lib.write_to_logs(err, logfile_name)
lib.docker_powercli_change_vm_ip_address(config.DNS().vm_name, config.DNS().ip, config.E2EP_ENVIRONMENT().subnet_mask, config.E2EP_ENVIRONMENT().default_gw)
err = "    Validating new ip address:"
lib.write_to_logs(err, logfile_name)
ip_address = lib.docker_powercli_get_vm_ip_address(config.DNS().vm_name)
err = "    IP address of "+config.DNS().vm_name+" is: "+ip_address
lib.write_to_logs(err, logfile_name)
err = "02. Change IP Address of Node Controller to config.DNS().ip Finished."
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# 03. Configure Tanium Prerequisites
err = "03. Configure Tanium Prerequisites Started."
lib.write_to_logs(err, logfile_name)
err = "    03A. Running paramiko_run_sh_on_remote_photon_vm():"
lib.write_to_logs(err, logfile_name)
err = "    03A. IP Address: "+config.DNS().ip
lib.write_to_logs(err, logfile_name)
err = "    03A. Username: "+config.PHOTONOS().username
lib.write_to_logs(err, logfile_name)
err = "    03A. Script: "+config.SCRIPTS().dns_configure_tanium_ip_tables_entrypoint+config.SCRIPTS().dns_configure_tanium_ip_tables_shscript
lib.write_to_logs(err, logfile_name)
lib.paramiko_run_sh_on_remote_photon_vm(config.DNS().ip, config.PHOTONOS().username, config.PHOTONOS().password, config.SCRIPTS().dns_configure_tanium_ip_tables_entrypoint, config.SCRIPTS().dns_configure_tanium_ip_tables_shscript)
seconds = 10
err = "    03B. Pausing for "+str(seconds)+" to allow networking configuration to take effect."
lib.write_to_logs(err, logfile_name)
lib.pause_python_for_duration(seconds)
err = "    03B. Resuming script."
lib.write_to_logs(err, logfile_name)
err = "03. Configure Tanium Prerequisites Finished."
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# 04. Install Tanium
err = "04. Install Tanium Started."
lib.write_to_logs(err, logfile_name)
err = "    04A. Running paramiko_run_sh_on_remote_photon_vm():"
lib.write_to_logs(err, logfile_name)
err = "    04A. IP Address: "+config.DNS().ip
lib.write_to_logs(err, logfile_name)
err = "    04A. Username: "+config.PHOTONOS().username
lib.write_to_logs(err, logfile_name)
err = "    04A. Script: "+config.SCRIPTS().dns_run_docker_compose_entrypoint+config.SCRIPTS().dns_run_docker_compose_shscript
lib.write_to_logs(err, logfile_name)
lib.paramiko_run_sh_on_remote_photon_vm(config.DNS().ip, config.PHOTONOS().username, config.PHOTONOS().password, config.SCRIPTS().dns_run_docker_compose_entrypoint, config.SCRIPTS().dns_run_docker_compose_shscript)
seconds = 60
err = "    04B. Pausing for "+str(seconds)+" to allow networking configuration to take effect."
lib.write_to_logs(err, logfile_name)
lib.pause_python_for_duration(seconds)
err = "    04B. Resuming script."
err = "04. Install Tanium Finished."
lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

