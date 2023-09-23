provider "vsphere" {
  user     = "administrator@vsphere.local"
  password = "VMware1!"
  vsphere_server = "172.16.0.10"
  allow_unverified_ssl = true
}

data "vsphere_datacenter" "datacenter" {
  name = "e2e"
}

data "vsphere_datastore" "datastore" {
  name          = "datastore1"
  datacenter_id = data.vsphere_datacenter.datacenter.id
}

data "vsphere_network" "network" {
  name          = "VM Network"
  datacenter_id = data.vsphere_datacenter.datacenter.id
}

resource "vsphere_virtual_machine" "vm" {
  name             = "tf-test-01"
  resource_pool_id = "resgroup-10"
  datastore_id     = data.vsphere_datastore.datastore.id
  num_cpus         = 1
  memory           = 1024
  guest_id         = "other3xLinux64Guest"
  network_interface {
    network_id = data.vsphere_network.network.id
  }
  disk {
    label = "disk0"
    size  = 20
  }
}
