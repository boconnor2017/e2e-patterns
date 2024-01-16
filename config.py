# Configuration for the E2E Patterns Lab
# Author: Brendan O'Connor
# Date: January 2024
# Version: 2.1 - added support for multiple hosts including ESXi 8

# Environment Variables (example: 172.16.0.0/24 subnet) - below are things that are part of your environment, editing these are REQUIRED
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
    photonos_username = "root" #default username to login to photon vms 
    photonos_password = "VMware1!VMware1!" #default password to login to photon vms
    photonos_source = "photon-ova-4.0-ca7c9e9330.ova"

'''
Below are variables that are created to manage the lab environment. Editing these are OPTIONAL.
- UNIVERSAL() is a class containing variables that are applied universally to a pattern
- LOGS() is a class containing variables that apply to logging
- DNS() is a class containing variables that apply to the DNS pattern
- VCSA() is a class containing variables that apply to the vcenter server pattern
- NSX() is a class containing variables that apply to the NSX pattern

IPAM: the recommended subnet size for this environment is /24
- x.x.x.01 = reserved for gateway
- x.x.x.02-08 = reserved for physical equipment
- x.x.x.200-254 = reserved for physical equipment
- x.x.x.09 = dns
- x.x.x.10 = vcsa
- x.x.x.11 = nsx
- x.x.x.12 = cloud builder 
'''

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

class PHOTONOS():
    pattern = "A-06: Build Photon Template from ISO"
    template_name = "photonos_4.0_template"

class MINIKUBE():
    pattern = "A-05: Kubernetes"
    photon_controller_vm_name = UNIVERSAL().vm_naming_convention+"-k8"
    template_vm_name = UNIVERSAL().vm_naming_convention+"-k8"
    ip = E2EP_ENVIRONMENT().subnet_prefix+"40"

class DNS():
    ip = "172.16.0.9"
    zone = "e2e.local"
    vm_name = UNIVERSAL().vm_naming_convention+"-002"
    photon_source = E2EP_ENVIRONMENT().photonos_source #Must be downloaded to /usr/local/drop of master controller
    port = "5380"

class VCSA():
    photon_controller_vm_name = UNIVERSAL().vm_naming_convention+"-003" 
    vcsa_vm_name = UNIVERSAL().vm_naming_convention+"-004"
    ip = E2EP_ENVIRONMENT().subnet_prefix+"10"
    domain_hostname = UNIVERSAL().fqdn_naming_convention+"vcsa-01"
    fqdn = domain_hostname+"."+DNS().zone
    photon_source = E2EP_ENVIRONMENT().photonos_source #Must be downloaded to /usr/local/drop of master controller
    sso_domain = "vsphere.local"
    json_filename = "/usr/local/e2e-patterns/vcsa/vcsa.json"
    username = "administrator@"+sso_domain
    datacenter = "e2e"

class ESXI():
    pattern = "C-01A: Add ESXi host to vCenter or C-01B: Building nested ESXi Host"
    username = "root"
    nested_esxi6_ova_source = "Nested_ESXi6.7u3_Appliance_Template_v1.ova" #Must be downloaded to /usr/local/drop of Master controller
    nested_esxi8_ova_source = "Nested_ESXi8.0u2_Appliance_Template_v1.ova" #Must be downloaded to /usr/local/drop of Master controller

class NSX():
    pattern = "C-02: NSX Manager"
    photon_controller_vm_name = UNIVERSAL().vm_naming_convention+"-005" 
    nsx_vm_name = UNIVERSAL().vm_naming_convention+"-006"
    ip = E2EP_ENVIRONMENT().subnet_prefix+"11"
    domain_hostname = UNIVERSAL().fqdn_naming_convention+"nsx-01"
    fqdn = domain_hostname+"."+DNS().zone
    photon_source = E2EP_ENVIRONMENT().photonos_source #Must be downloaded to /usr/local/drop of master controller
    mgrformfactor = "small"
    password = UNIVERSAL().password+UNIVERSAL().password
    nsx_ova_source = "nsx-unified-appliance-3.2.1.2.0.20541216.ova" #Must be downloaded to /usr/local/drop of photon controller
    nsx_terraform_source = UNIVERSAL().home_dir+"/terraform/install-nsx-manager/main.tf"
    main_tf_git_url = "https://raw.githubusercontent.com/boconnor2017/e2e-patterns/main/terraform/install-nsx-manager/main.tf"
    local_py_git_url = "https://raw.githubusercontent.com/boconnor2017/e2e-patterns/main/terraform/install-nsx-manager/local.py"
    local_py_local_dir = "/usr/local/drop/local.py"
    main_tf_local_dir = "/usr/local/drop/main.tf"

class CLOUD_BUILDER():
    pattern = "C-03: Cloud Builder"
    photon_controller_vm_name = UNIVERSAL().vm_naming_convention+"-007"
    cb_vm_name = UNIVERSAL().vm_naming_convention+"-008"
    cb_ova_source = "VMware-Cloud-Builder-5.0.0.0-21822418_OVF10.ova" #Must be downloaded to /usr/local/drop of photon controller
    ip = E2EP_ENVIRONMENT().subnet_prefix+"12"
    domain_hostname = UNIVERSAL().fqdn_naming_convention+"vcfcb-01"
    fqdn = domain_hostname+"."+DNS().zone
    photon_source = E2EP_ENVIRONMENT().photonos_source #Must be downloaded to /usr/local/drop of master controller
    password = UNIVERSAL().password+UNIVERSAL().password    
    terraform_source = UNIVERSAL().home_dir+"/terraform/install-vcf-cb/main.tf"
    main_tf_git_url = "https://raw.githubusercontent.com/boconnor2017/e2e-patterns/main/terraform/install-vcf-cb/main.tf"
    local_py_git_url = "https://raw.githubusercontent.com/boconnor2017/e2e-patterns/main/terraform/install-vcf-cb/local.py"
    local_py_local_dir = "/usr/local/drop/local.py"
    main_tf_local_dir = "/usr/local/drop/main.tf"
