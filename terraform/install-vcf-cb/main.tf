# main.tf

provider "vsphere" {
  user     = "administrator@vsphere.local"
  password = "VMware1!"
  vsphere_server = "172.16.0.10"
  allow_unverified_ssl = true
}

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
      "FIPS_ENABLE"              = var.FIPS_ENABLE,
      "guestinfo.ADMIN_PASSWORD" = var.guestinfo_ADMIN_PASSWORD,
      "guestinfo.ADMIN_USERNAME" = var.guestinfo_ADMIN_USERNAME,
      "guestinfo.DNS"            = var.guestinfo_DNS,
      "guestinfo.domain"         = var.guestinfo_domain,
      "guestinfo.gateway"        = var.guestinfo_gateway,
      "guestinfo.hostname"       = var.guestinfo_hostname,
      "guestinfo.ip0"            = var.guestinfo_ip0,
      "guestinfo.netmask0"       = var.guestinfo_netmask0,
      "guestinfo.ntp"            = var.guestinfo_ntp,
      "guestinfo.ROOT_PASSWORD"  = var.guestinfo_ROOT_PASSWORD,
      "guestinfo.searchpath"     = var.guestinfo_searchpath,
      "vm.vmname"                = var.vm_vmname
    }
  }
}
