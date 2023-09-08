# Configuration for the E2E Patterns Lab
# Author: Brendan O'Connor
# Date: September 2023
# Version: 2.0

# Environment Variables (example: 172.16.0.0/24 subnet) - below are things that are part of your environment, editing these are REQUIRED
class E2EP_ENVIRONMENT():
	subnet_mask = "255.255.255.0"
	subnet_size = "24" #CIDR block, default /24 (/24 recommended)
	subnet_prefix = "172.16.0." #first four numbers of the subnet
	default_gw = subnet_prefix+"1" #default: .01 gateway address
	ntp_server = "pool.ntp.org"
	esxi_host_ip = subnet_prefix+"201" 
	esxi_host_username = "root" #default username to login to esxi host
	esxi_host_password = "VMware1!" #password to login to esxi host
	esxi_host_datastore = "datastore1" #datastore that will be used as the target storage for patterns
	esxi_host_virtual_switch = "VM Network" #virtual switch that will be used as the target port group for patterns
	photonos_username = "root" #default username to login to photon vms 
	photonos_password = "VMware1!VMware1!" #default password to login to photon vms

'''
Below are variables that are created to manage the lab environment. Editing these are OPTIONAL.
- UNIVERSAL() is a class containing variables that are applied universally to a pattern
- LOGS() is a class containing variables that apply to logging
- DNS() is a class containing variables that apply to the DNS pattern
- VCSA() is a class containing variables that apply to the vcenter server pattern

IPAM: the recommended subnet size for this environment is /24
- x.x.x.01 = reserved for gateway
- x.x.x.02-08 = reserved for physical equipment
- x.x.x.200-254 = reserved for physical equipment
- x.x.x.09 = dns
- x.x.x.10 = vcsa
- x.x.x.11 = nsx
- x.x.x.12 = aria lifecycle manager 
- x.x.x.13 = vmware identity manager 
- x.x.x.14 = aria automation
- x.x.x.15 = aria operations 
- x.x.x.16 = aria operations for logs (Log Insight)
- x.x.x.17 = aria saltstack master
- x.x.x.18 = reserved for additional aria appliances
- x.x.x.19 = reserved for additional aria appliances
- x.x.x.20 = reserved for nested esxi
- x.x.x.21 = reserved for nested esxi
- x.x.x.22 = reserved for nested esxi
- x.x.x.23 = reserved for nested esxi
- x.x.x.24 = reserved for nested esxi
- x.x.x.25 = reserved for NSX edge / Avi appliances
- x.x.x.26 = reserved for NSX edge / Avi appliances
- x.x.x.27 = reserved for NSX edge / Avi appliances
- x.x.x.28 = reserved for NSX edge / Avi appliances
- x.x.x.29 = reserved for NSX edge / Avi appliances
- x.x.x.30 = reserved for aria workloads under management
- x.x.x.31 = reserved for aria workloads under management
- x.x.x.32 = reserved for aria workloads under management
- x.x.x.33 = reserved for aria workloads under management
- x.x.x.34 = reserved for aria workloads under management
- x.x.x.35 = reserved for aria workloads under management
- x.x.x.36 = reserved for aria workloads under management
- x.x.x.37 = reserved for aria workloads under management
- x.x.x.38 = reserved for aria workloads under management
- x.x.x.39 = reserved for aria workloads under management
'''

class UNIVERSAL():
    password = "VMware1!"
    vm_naming_convention = "e2ep"
    fqdn_naming_convention = "vmw"
	
class LOGS():
	template = "_template.log"
	dns = "_dns.log"
	nfs = "_nfs.log"
	mvc = "_mvc.log"
	mnsx = "_mnsx.log"
	photonos = "_photonos.log"
	minikube = "_k8.log"
	vcsa = "_vcsa.log"

class DNS():
    ip = "172.16.0.9"
    zone = "e2e.local"
    vm_name = UNIVERSAL().vm_naming_convention+"-002"
    photon_source = "photon-ova-4.0-ca7c9e9330.ova" #Must be downloaded to /usr/local/drop of master controller
    port = "5380"

class VCSA():
    photon_controller_vm_name = UNIVERSAL().vm_naming_convention+"-003" 
    vcsa_vm_name = UNIVERSAL().vm_naming_convention+"-004"
    ip = E2EP_ENVIRONMENT().subnet_prefix+"10"
    fqdn = UNIVERSAL().fqdn_naming_convention+"vcsa-01"
    photon_source = "photon-ova-4.0-ca7c9e9330.ova" #Must be downloaded to /usr/local/drop of master controller
    sso_domain = "vsphere.local"
    json_filename = "/usr/local/e2e-patterns/vcsa/vcsa.json"
    
