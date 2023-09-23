# main.tf

provider "vsphere" {
  user     = "administrator@vsphere.local"
  password = "VMware1!"
  vsphere_server = "172.16.0.10"
  allow_unverified_ssl = true
}

# vSphere Infrastructure Details
variable "data_center" { default = "e2e" }
variable "vds" { default = "VM Network" }
variable "workload_datastore" { default = "datastore1" }
variable "compute_host" {default = "172.16.0.201"}
variable "vsphere_server" {default = "172.16.0.10"}

# vCenter Credential Variables
variable "vsphere_user" { default = "administrator@vsphere.local"}
variable "vsphere_password" { default = "VMware1!"}

# NSX-T Manager Deployment
variable "mgmt_pg" { default = "VM Network" }
variable "vm_name" { default = "nsx-test-01" }
variable "local_ovf_path" { default = "/usr/local/drop/nsx-unified-appliance-3.2.1.2.0.20541216.ova" }
variable "deployment_option" { default = "small" } # valid deployments are: extra_small, small, medium, large
variable "nsx_role" { default = "NSX Manager" }          # valid roles are NSX Manager, NSX Global Manager
variable "nsx_ip_0" { default = "172.16.0.11" }
variable "nsx_netmask_0" { default = "255.255.255.0" }
variable "nsx_gateway_0" { default = "172.16.0.1" }
variable "nsx_dns1_0" { default = "172.16.0.9" }
variable "nsx_domain_0" { default = "e2e.local" }
variable "nsx_ntp_0" { default = "pool.ntp.org" }
variable "nsx_isSSHEnabled" { default = "True" }
variable "nsx_allowSSHRootLogin" { default = "True" }
variable "nsx_passwd_0" { default = "VMware1!VMware1!" }
variable "nsx_cli_passwd_0" { default = "VMware1!VMware1!" }
variable "nsx_cli_audit_passwd_0" { default = "VMware1!VMware1!" }
variable "nsx_hostname" { default = "vmwnsx-01.e2e.local" }

# Data source for vCenter Datacenter
data "vsphere_datacenter" "datacenter" {
  name = var.data_center
}
 
# Data source for vCenter Cluster
#data "vsphere_compute_cluster" "cluster" {
#  name          = var.cluster
#  datacenter_id = data.vsphere_datacenter.datacenter.id
#}
 
# Data source for vCenter Datastore
data "vsphere_datastore" "datastore" {
  name          = var.workload_datastore
  datacenter_id = data.vsphere_datacenter.datacenter.id
}
 
# Data source for vCenter Portgroup
data "vsphere_network" "mgmt" {
  name          = var.mgmt_pg
  datacenter_id = data.vsphere_datacenter.datacenter.id
}
 
# Data source for vCenter Resource Pool. In our case we will use the root resource pool
#data "vsphere_resource_pool" "pool" {
#  name          = format("%s%s", data.vsphere_compute_cluster.cluster.name, "/Resources")
#  datacenter_id = data.vsphere_datacenter.datacenter.id
#}
 
# Data source for ESXi host to deploy to
data "vsphere_host" "host" {
  name          = var.compute_host
  datacenter_id = data.vsphere_datacenter.datacenter.id
}
 
# Data source for the OVF to read the required OVF Properties
data "vsphere_ovf_vm_template" "ovfLocal" {
  name             = var.vm_name
  resource_pool_id = "resgroup-10"
  datastore_id     = data.vsphere_datastore.datastore.id
  host_system_id   = data.vsphere_host.host.id
  local_ovf_path   = var.local_ovf_path
  ovf_network_map = {
    "Network 1" = data.vsphere_network.mgmt.id
  }
}
 
# Deployment of VM from Local OVA
resource "vsphere_virtual_machine" "nsxt01" {
  name                 = var.vm_name
  datacenter_id        = data.vsphere_datacenter.datacenter.id
  datastore_id         = data.vsphere_ovf_vm_template.ovfLocal.datastore_id
  host_system_id       = data.vsphere_ovf_vm_template.ovfLocal.host_system_id
  resource_pool_id     = data.vsphere_ovf_vm_template.ovfLocal.resource_pool_id
  num_cpus             = data.vsphere_ovf_vm_template.ovfLocal.num_cpus
  num_cores_per_socket = data.vsphere_ovf_vm_template.ovfLocal.num_cores_per_socket
  memory               = data.vsphere_ovf_vm_template.ovfLocal.memory
  guest_id             = data.vsphere_ovf_vm_template.ovfLocal.guest_id
  scsi_type            = data.vsphere_ovf_vm_template.ovfLocal.scsi_type
  dynamic "network_interface" {
    for_each = data.vsphere_ovf_vm_template.ovfLocal.ovf_network_map
    content {
      network_id = network_interface.value
    }
  }
 
  wait_for_guest_net_timeout = 5
 
  ovf_deploy {
    allow_unverified_ssl_cert = true
    local_ovf_path            = var.local_ovf_path
    disk_provisioning         = "thin"
    deployment_option         = var.deployment_option
 
  }
  vapp {
    properties = {
      "nsx_role"               = var.nsx_role,
      "nsx_ip_0"               = var.nsx_ip_0,
      "nsx_netmask_0"          = var.nsx_netmask_0,
      "nsx_gateway_0"          = var.nsx_gateway_0,
      "nsx_dns1_0"             = var.nsx_dns1_0,
      "nsx_domain_0"           = var.nsx_domain_0,
      "nsx_ntp_0"              = var.nsx_ntp_0,
      "nsx_isSSHEnabled"       = var.nsx_isSSHEnabled,
      "nsx_allowSSHRootLogin"  = var.nsx_allowSSHRootLogin,
      "nsx_passwd_0"           = var.nsx_passwd_0,
      "nsx_cli_passwd_0"       = var.nsx_cli_passwd_0,
      "nsx_cli_audit_passwd_0" = var.nsx_cli_audit_passwd_0,
      "nsx_hostname"           = var.nsx_hostname
    }
  }
  lifecycle {
    ignore_changes = [
      #vapp # Enable this to ignore all vapp properties if the plan is re-run
      vapp[0].properties["nsx_role"], # Avoid unwanted changes to specific vApp properties.
      vapp[0].properties["nsx_passwd_0"],
      vapp[0].properties["nsx_cli_passwd_0"],
      vapp[0].properties["nsx_cli_audit_passwd_0"],
      host_system_id # Avoids moving the VM back to the host it was deployed to if DRS has relocated it
    ]
  }
}
