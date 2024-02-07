#!/bin/sh
# PowerCLI Script to deploy a custom nested esxi 8 host (vCenter required)
# Author: Brendan O'Connor
# Date: January 2024

# Capture input from command line 
# 00: vCenter Server
# 01: vCenter User (administrator@vsphere.local recommended)
# 02: vCenter Password
# 03: ESXi Host where OVA will be deployed
# 04: Path to photon ova binaries 
# 05: Name of the virtual machine
# 06: Number of CPUs
# 07: Memory (MB)
# 08: Hostname 
# 09: IP Address
# 10: Netmask 
# 11: Gateway
# 12: DNS (comma separated ip addresses)
# 13: Domain (e2e.local)
# 14: NTP Server 
# 15: Password

param(
[string]$a
)

# Parse Command Line Inputs
$b = $a.Split(" ")

# Connect to vCenter
Connect-VIServer -Server $b[0] -Protocol https -User $b[1] -Password $b[2] -Force

# Photon parameters (optional - DHCP if left blank)
$photon_params = Get-OvfConfiguration -Ovf $b[4]
$photon_params.Common.guestinfo.hostname.Value = $b[8]
$photon_params.Common.guestinfo.ipaddress.Value = $b[9]
$photon_params.Common.guestinfo.netmask.Value = $b[10]
$photon_params.Common.guestinfo.gateway.Value = $b[11]
#$photon_params.Common.guestinfo.vlan.Value = ""
$photon_params.Common.guestinfo.dns.Value = $b[12]
$photon_params.Common.guestinfo.domain.Value = $b[13]
$photon_params.Common.guestinfo.ntp.Value = $b[14]
#$photon_params.Common.guestinfo.syslog.Value = ""
$photon_params.Common.guestinfo.password.Value = $b[15]
$photon_params.Common.guestinfo.ssh_key.Value = true
#$photon_params.Common.guestinfo.ssh.Value = ""
#$photon_params.Common.guestinfo.createvmfs.Value = ""
#$photon_params.Common.guestinfo.followmac.Value = ""
#$photon_params.Common.guestinfo.debug.Value = ""
#$photon_params.NetworkMapping.VM_Network.Value = ""
# To use, add -OvfConfiguration $photon_params to the Import-VApp line below

Import-VApp -VMHost $b[3] -Source $b[4] -Name $b[5] -OvfConfiguration $photon_params -Force 
Set-VM -VM $b[5] -NumCPU $b[6] -MemoryMB $b[7] -Confirm:$false
Start-VM -VM $b[5]
