# Configuration for the E2E Patterns Lab
# Author: Brendan O'Connor
# Date: August 2023

# Environment Variables (example: 172.16.0.0/24 subnet) - below are things that are part of your environment, editing these are REQUIRED
class E2EP_ENVIRONMENT():
	subnet_mask = "255.255.255.0"
	subnet_size = "24" #CIDR block, default /24
	subnet_prefix = "172.16.0." #first four numbers of the subnet
	default_gw = subnet_prefix+"1" #default: .01 gateway address
	ntp_server = "pool.ntp.org"
	esxi_host_ip = subnet_prefix+"201" 
	esxi_host_username = "root" #default username to login to esxi host
	esxi_host_password = "VMware1!" #password to login to esxi host
	esxi_host_datastore = "datastore1" #datastore that will be used as the target storage for patterns
	esxi_host_virtual_switch = "VM Network" #virtual switch that will be used as the target port group for patterns

# Lab Variables - below are things that will be created as part of the automation, editing these are OPTIONAL 
class LOGS():
	dns = "_dns.log"
	nfs = "_nfs.log"
	mvc = "_mvc.log"
	mnsx = "_mnsx.log"

class DNS():
	ip = "172.16.0.9"
	zone = "e2e.local"

class IPAM():
	fqdn = [
		"esxi01"+"."+DNS().zone, # ESXi Host
		"lab-nfs-001"+"."+DNS().zone, # NFS Server
		"lab-vc-000"+"."+DNS().zone, # MGT vCenter
		"lab-vc-001"+"."+DNS().zone, # Site A vCenter
		"lab-nsxm-000"+"."+DNS().zone, # MGT NSX Manager
		"lab-vesxi-001"+"."+DNS().zone, # Nested ESXi 1
		"lab-vesxi-002"+"."+DNS().zone, # Nested ESXi 2
		"lab-vesxi-003"+"."+DNS().zone, # Nested ESXi 3
		"lab-vesxi-004"+"."+DNS().zone, # Nested ESXi 4
		"@"+"."+DNS().zone, # The zone itself 
		"" #Last one Blank
	]
	ip = [
		E2EP_ENVIRONMENT().esxi_host_ip, # ESXi Host
		"172.16.0.10", # NFS Server
		"172.16.0.23", # MGT vCenter
		"172.16.0.22", # Site A vCenter
		"172.16.0.24", # MGT NSX Manager
		"172.16.0.30", # Nested ESXi 1
		"172.16.0.31", # Nested ESXi 2
		"172.16.0.32", # Nested ESXi 3
		"172.16.0.33", # Nested ESXi 4
		DNS().ip, # The zone itself 
		"" #Last one Blank
	]
	tag = [
		"PESXI", # ESXi Host
		"NFS", # NFS Server
		"MGT_VC", # MGT vCenter
		"SITEA_VC", # Site A vCenter
		"MGT_NSX", # MGT NSX Manager 
		"VESXi", # Nested ESXi 1
		"VESXi", # Nested ESXi 2
		"VESXi", # Nested ESXi 3
		"VESXi", # Nested ESXi 4
		"DNS", # The zone itself
		"" #Last one Blank
	]
