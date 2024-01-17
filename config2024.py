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

# Basic PhotonOS Pattern variables
class MINIKUBE():
    pattern = "A-04: Kubernetes"
    photon_controller_vm_name = UNIVERSAL().vm_naming_convention+"-k8"
    template_vm_name = UNIVERSAL().vm_naming_convention+"-k8"
    ip = E2EP_ENVIRONMENT().subnet_prefix+"40"

class PHOTONOS():
    pattern = "A-06: Build Photon Template from ISO"
    template_name = "photonos_4.0_template"

# Shared Services Pattern variables
class DNS():
    ip = "172.16.0.9"
    zone = "e2e.local"
    vm_name = UNIVERSAL().vm_naming_convention+"-002"
    photon_source = E2EP_ENVIRONMENT().photonos_source #Must be downloaded to /usr/local/drop of master controller
    port = "5380"
