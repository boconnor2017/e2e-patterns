# E2E deploy ova 
# Author: Brendan O'Connor  

provider "vsphere" {
  user     = var.vsphere_user
  password = var.vsphere_pass
  vsphere_server = var.vsphere_serer
  allow_unverified_ssl = true
}

data "vsphere_datacenter" "datacenter" {
  name = var.datacenter_name
}

data "vsphere_datastore" "datastore" {
  name          = var.datastore_name
  datacenter_id = data.vsphere_datacenter.datacenter.id
}

data "vsphere_compute_cluster" "cluster" {
  name          = var.vsphere_compute_cluster_name
  datacenter_id = data.vsphere_datacenter.datacenter.id
}

data "vsphere_resource_pool" "default" {
  name          = format("%s%s", data.vsphere_compute_cluster.cluster.name, "/Resources/Workload")
  datacenter_id = data.vsphere_datacenter.datacenter.id
}

data "vsphere_host" "host" {
  name          = var.esxi_host_name
  datacenter_id = data.vsphere_datacenter.datacenter.id
}

data "vsphere_network" "network" {
  name          = var.network_name
  datacenter_id = data.vsphere_datacenter.datacenter.id
}

data "vsphere_ovf_vm_template" {
  name              = "Nested_ESXi8.0u2_Appliance_Template_v2"
  disk_provisioning = "thin"
  resource_pool_id  = data.vsphere_host.host.resource_pool_id
  datastore_id      = data.vsphere_datastore.datastore.id
  host_system_id    = data.vsphere_host.host.id
  remote_ovf_url    = "https://download3.vmware.com/software/vmw-tools/nested-esxi/Nested_ESXi8.0u2_Appliance_Template_v2.ova"
  ovf_network_map = {
      network_id = data.vsphere_network.network.id
  }
}

resource "vsphere_virtual_machine" {
  name                 = var.vm_name
  datacenter_id        = data.vsphere_datacenter.datacenter.id
  datastore_id         = data.vsphere_datastore.datastore.id
  host_system_id       = data.vsphere_host.host.id
  resource_pool_id     = data.vsphere_host.host.resource_pool_id
  num_cpus             = var.cpu
  memory               = var.memory
  guest_id             = var.guest
  dynamic "network_interface" {
      for_each = data.vsphere_ovf_vm_template.ovf_network_map
      content {
          network_id = network_interface.value
      }
  }
  wait_for_guest_net_timeout = 0
  wait_for_guest_ip_timeout  = 0

  ovf_deploy {
      allow_unverified_ssl_cert = false
      remote_ovf_url            = data.vsphere_ovf_vm_template.remote_ovf_url
      disk_provisioning         = data.vsphere_ovf_vm_template.disk_provisioning
      ovf_network_map           = data.vsphere_ovf_vm_template.ovf_network_map
  }

vapp {
  properties = {
      "guestinfo.hostname" = var.hostname,
      "guestinfo.ipaddress" = var.ip_address,
      "guestinfo.netmask" = var.netmask,
      "guestinfo.gateway" = var.default_gateway,
      "guestinfo.dns" = var.dns,
      "guestinfo.domain" = var.domain,
      "guestinfo.ntp" = var.ntp,
      "guestinfo.password" = var.guest_password,
      "guestinfo.ssh" = "True"
      }
  }

  lifecycle {
      ignore_changes = [
      annotation,
      disk[0].io_share_count,
      disk[1].io_share_count,
      disk[2].io_share_count,
      vapp[0].properties,
      ]
  }
}

