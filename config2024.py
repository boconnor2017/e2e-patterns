# Configuration for the E2E Patterns Lab 2024
# Author: Brendan O'Connor
# Date: January 2024
# Version: 3.0

'''
Below are variables that are created to manage the lab environment. 
- UNIVERSAL() is a class containing variables that are applied universally to a pattern.
- LOGS() is a class containing variables that apply to logging.
- TEMPLATE() is a class used by default.
- SCRIPTS() is a class used to pull various scripts used by A patterns.
- DNS() is a class containing variables that apply to the DNS pattern.
- VCSA() is a class containing variables that apply to the vcenter server pattern.
- NSX() is a class containing variables that apply to the NSX pattern.

The recommended subnet size to support the e2e-patterns lab is /24.
The subnet must be configured on the physical network. 
The following IP ranges are used for this lab by default. 
- x.x.x.01-08 = reserved for physical equipment
- x.x.x.200-254 = reserved for physical equipment
- x.x.x.09 = dns
- x.x.x.10 = vcsa
- x.x.x.11 = nsx
'''

class E2EP_ENVIRONMENT():
    subnet_mask = "255.255.255.0"
    subnet_size = "24" #CIDR block, default /24 (/24 recommended)
    subnet_prefix = "172.16.0." #first four numbers of the subnet
    default_gw = subnet_prefix+"1" #default: .01 gateway address
    ntp_server = "pool.ntp.org"
    esxi_host_ip = subnet_prefix+"201" #ESXi6 supported CPU
    esxi8_host_ip = subnet_prefix+"203" #ESXi8 supported CPU
    esxi_host_username = "root" #default username to login to esxi host
    esxi_host_password = "VMware1!" #password to login to esxi host
    esxi_host_datastore = "datastore1" #datastore that will be used as the target storage for patterns
    esxi_host_virtual_switch = "VM Network" #virtual switch that will be used as the target port group for patterns

class UNIVERSAL():
    github_repo = "https://github.com/boconnor2017/e2e-patterns"
    home_dir = "/usr/local/e2e-patterns"
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
    minikube = "_minikube.log"
    vcsa = "_vcsa.log"
    nsx = "_nsx.log"
    aria = "_aria.log"
    vcf = "_vcf.log"
    esxi = "_esxi.log"

class TEMPLATE():
    pattern = "A-00: Template"
    photon_controller_vm_name = UNIVERSAL().vm_naming_convention+"-template"
    template_vm_name = UNIVERSAL().vm_naming_convention+"-template"
    ip = E2EP_ENVIRONMENT().subnet_prefix+"250"

class SCRIPTS():
    create_vm_with_powercli_url = "https://raw.githubusercontent.com/boconnor2017/e2e-patterns/main/powershell/create_vm_with_powercli.ps1"
    create_vm_with_powercli_filename = "create_vm_with_powercli.ps1"
    get_vm_ip_with_powercli_url = "https://raw.githubusercontent.com/boconnor2017/e2e-patterns/main/powershell/get_vm_ip.ps1"
    get_vm_ip_with_powercli_filename = "get_vm_ip.ps1"
    change_photonos_default_password_with_powercli_url = "https://raw.githubusercontent.com/boconnor2017/e2e-patterns/main/powershell/change_photonos_default_password_with_powershell.ps1"
    change_photonos_default_password_with_powercli_filename = "change_photonos_default_password_with_powershell.ps1"
    change_vm_ip_with_powercli_url = "https://raw.githubusercontent.com/boconnor2017/e2e-patterns/main/powershell/change_vm_ip_with_powercli.ps1"
    change_vm_ip_with_powercli_filename = "change_vm_ip_with_powercli.ps1"
    refresh_e2e_patterns_url = "https://raw.githubusercontent.com/boconnor2017/e2e-patterns/main/refresh-e2e-patterns.sh"
    refresh_e2e_patterns_filename = "refresh-e2e-patterns.sh"
    photon_prep_script_url = "https://raw.githubusercontent.com/boconnor2017/e2e-patterns/main/prep-photon.sh"
    photon_prep_script_filename = "prep-photon.sh"
    dns_configure_tanium_ip_tables_entrypoint = "/usr/local/e2e-patterns/dns/"
    dns_configure_tanium_ip_tables_shscript = "configure-tanium-ip-tables.sh"
    dns_run_docker_compose_entrypoint = "/usr/local/e2e-patterns/dns/"
    dns_run_docker_compose_shscript = "run-docker-compose.sh"
    get_vm_list_with_powercli_url = "https://raw.githubusercontent.com/boconnor2017/e2e-patterns/main/powershell/get_vm_list_with_powercli.ps1"
    get_vm_list_with_powercli_filename = "get_vm_list_with_powercli.ps1"
    attach_iso_to_vm_with_powercli_url = "https://raw.githubusercontent.com/boconnor2017/e2e-patterns/main/powershell/attach_iso_to_vm_with_powercli.ps1"
    attach_iso_to_vm_with_powercli_filename = "attach_iso_to_vm_with_powercli.ps1"

# Basic PhotonOS Pattern variables
class MINIKUBE():
    pattern = "A-04: Kubernetes"
    photon_controller_vm_name = UNIVERSAL().vm_naming_convention+"-k8"
    template_vm_name = UNIVERSAL().vm_naming_convention+"-k8"
    ip = E2EP_ENVIRONMENT().subnet_prefix+"40"

class PHOTONOS():
    pattern = "A-06: Build Photon Template from OVA using ovftool"
    template_name = "photonos_4.0_template"
    username = "root" #default username to login to photon vms 
    password = "VMware1!VMware1!" #default password to login to photon vms
    source = "photon-ova-4.0-ca7c9e9330.ova"

class DNS():
    pattern = "B-01: Containerized DNS Server"
    ip = "172.16.0.9"
    zone = "e2e.local"
    vm_name = UNIVERSAL().vm_naming_convention+"-002"
    photon_source = PHOTONOS().source #Must be downloaded to /usr/local/drop of master controller
    port = "5380"

class VCSA():
    pattern = "C-01: vCenter Server"
    photon_controller_vm_name = UNIVERSAL().vm_naming_convention+"-003" 
    vcsa_vm_name = UNIVERSAL().vm_naming_convention+"-004"
    ip = E2EP_ENVIRONMENT().subnet_prefix+"10"
    domain_hostname = UNIVERSAL().fqdn_naming_convention+"vcsa-01"
    fqdn = domain_hostname+"."+DNS().zone
    sso_domain = "vsphere.local"
    json_filepath = "/usr/local/e2e-patterns/vcsa/"
    json_filename = "vcsa.json"
    username = "administrator@"+sso_domain
    datacenter = "e2e"
    iso_folder_on_datastore = "ISO\\"
    iso_name = "VMware-VCSA-all-8.0.0-20519528.iso"
