#!/bin/sh
# PowerCLI Script to deploy a nested ESXi host (vCenter required)
# Author: Brendan O'Connor
# Date: January 2024

# Capture input from command line 
# 0: vCenter Server
# 1: vCenter User (administrator@vsphere.local recommended)
# 2: vCenter Password
# 3: ESXi Host where OVA will be deployed
# 4: Path to Nested ESXi ova binaries 
# 5: Name of the virtual machine
# 6: Number of CPUs
# 7: Memory (MB)


param(
[string]$a
)

# Parse Command Line Inputs
$b = $a.Split(" ")

# Connect to vCenter
Connect-VIServer -Server $b[0] -Protocol https -User $b[1] -Password $b[2] -Force

# Photon parameters (optional - DHCP if left blank)
#$photon_params = Get-OvfConfiguration -Ovf $b[4]
#$photon_params.Common.guestinfo.hostname.Value = ""
#$photon_params.Common.guestinfo.ipaddress.Value = ""
#$photon_params.Common.guestinfo.netmask.Value = ""
#$photon_params.Common.guestinfo.gateway.Value = ""
#$photon_params.Common.guestinfo.vlan.Value = ""
#$photon_params.Common.guestinfo.dns.Value = ""
#$photon_params.Common.guestinfo.domain.Value = ""
#$photon_params.Common.guestinfo.ntp.Value = ""
#$photon_params.Common.guestinfo.syslog.Value = ""
#$photon_params.Common.guestinfo.password.Value = ""
#$photon_params.Common.guestinfo.ssh_key.Value = ""
#$photon_params.Common.guestinfo.ssh.Value = ""
#$photon_params.Common.guestinfo.createvmfs.Value = ""
#$photon_params.Common.guestinfo.followmac.Value = ""
#$photon_params.Common.guestinfo.debug.Value = ""
#$photon_params.NetworkMapping.VM_Network.Value = ""
# To use, add -OvfConfiguration $photon_params to the Import-VApp line below

Import-VApp -VMHost $b[3] -Source $b[4] -Name $b[5] -Force 
Set-VM -VM $b[5] -NumCPU $b[6] -MemoryMB $b[7] -Confirm:$false
Start-VM -VM $b[5]
