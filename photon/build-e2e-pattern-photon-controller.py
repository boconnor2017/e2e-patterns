import lib
import config 

photon_ip_address = "172.16.0.178"
logfile_name = "_test.log"

# Test SSH Connection to photon
err = "Testing SSH connection to "+photon_ip_address
lib.write_to_logs(err, logfile_name)
ssh_test = lib.connect_to_ssh_server_test(photon_ip_address, config.E2EP_ENVIRONMENT().photonos_username, config.E2EP_ENVIRONMENT().photonos_password)
if ssh_test:
	err = "   connection succeeded."
	lib.write_to_logs(err, logfile_name)
else:
	err = "[!] connection failed"
	lib.write_to_logs(err, logfile_name)
err = ""
lib.write_to_logs(err, logfile_name)

# Download prep-photon scripts
if ssh_test:
    err = "Downloading photon prep scripts."
    lib.write_to_logs(err, logfile_name)
    lib.download_photon_prep_script_via_ssh(photon_ip_address, config.E2EP_ENVIRONMENT().photonos_username, config.E2EP_ENVIRONMENT().photonos_password)
    err = ""
    lib.write_to_logs(err, logfile_name)

# Validate prep-photon script
if ssh_test:
    err = "Pulling prep script into variable"
    lib.write_to_logs(err, logfile_name)
    prep_photon_script_source = "/usr/local/prep-photon.sh"
    prep_photon_script_txt = lib.populate_var_from_file(prep_photon_script_source)
    prep_photon_script_commands = prep_photon_script_txt.split('\n')
    err = "Validating Commands:"
    lib.write_to_logs(err, logfile_name)
    i=0
    for commands in prep_photon_script_commands:
        err = "    ["+str(i)+"] "+commands
        lib.write_to_logs(err, logfile_name)
        i=i+1

err = ""
lib.write_to_logs(err, logfile_name)

# Run prep-photon script
if ssh_test:
    err = "Pulling prep script into variable"
    lib.write_to_logs(err, logfile_name)
    prep_photon_script_source = "/usr/local/prep-photon.sh"
    prep_photon_script_txt = lib.populate_var_from_file(prep_photon_script_source)
    prep_photon_script_commands = prep_photon_script_txt.split('\n')
    err = "Running Commands:"
    lib.write_to_logs(err, logfile_name)
    i=0
    for commands in prep_photon_script_commands:
        err = "    Running: ["+str(i)+"] "+commands
        lib.write_to_logs(err, logfile_name)
        stdout = lib.send_command_over_ssh(commands, photon_ip_address, config.E2EP_ENVIRONMENT().photonos_username, config.E2EP_ENVIRONMENT().photonos_password)
        i=i+1

err = "Finished."
lib.write_to_logs(err, logfile_name)
