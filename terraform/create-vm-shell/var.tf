# var file for create-vm-shell

#VM Target
variable "vsphere_user" { default = "root" }
variable "vsphere_pass" { default = "VMware1!" }
variable "vsphere_serer" { default = "172.16.0.201" }
variable "datacenter_name" { default = "ha-datacenter" }
variable "datastore_name" { default = "datastore1" }
variable "network_name" { default = "VM Network" }
variable "esxi_host_name" { default = "esxi1" }

# VM Configuration Details
variable "vm_name" { default = "tf-test-02" }
variable "cpu" { default = 1 }
variable "memory" { default = 1024 }
variable "guest" { default = "other3xLinux64Guest" }
