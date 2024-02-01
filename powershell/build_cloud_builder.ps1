#!/bin/sh
# PowerCLI Script to deploy cloud builder 5.1 (vCenter required)
# Author: Brendan O'Connor
# Date: February 2024
# Version: 1.0

# Capture input from command line 
# 00: vCenter Server
# 01: vCenter User (administrator@vsphere.local recommended)
# 02: vCenter Password
# 03: ESXi Host where OVA will be deployed
# 04: Path to cloud builder ova binaries 
# 05: Name of the virtual machine
# 06: Hostname 
# 07: IP Address
# 08: Netmask 
# 09: Gateway
# 10: DNS (comma separated ip addresses)
# 11: Domain (e2e.local)
# 12: NTP Server 
# 13: Password

param(
[string]$a
)

# Parse Command Line Inputs
$b = $a.Split(" ")

# Connect to vCenter
Connect-VIServer -Server $b[0] -Protocol https -User $b[1] -Password $b[2] -Force

# Photon parameters (optional - DHCP if left blank)
$cb_params = Get-OvfConfiguration -Ovf $b[4]
$cb_params.Common.guestinfo.ADMIN_USERNAME.Value = "admin"
$cb_params.Common.guestinfo.ADMIN_PASSWORD.Value = $b[12]
$cb_params.Common.guestinfo.ROOT_PASSWORD.Value = $b[12]
$cb_params.Common.guestinfo.hostname.Value = $b[6]
$cb_params.Common.guestinfo.ip0.Value = $b[7]
$cb_params.Common.guestinfo.netmask0.Value = $b[8]
$cb_params.Common.guestinfo.gateway.Value = $b[9]
$cb_params.Common.guestinfo.DNS.Value = $b[10]
$cb_params.Common.guestinfo.domain.Value = $b[11]
$cb_params.Common.guestinfo.searchpath.Value = $b[11]
$cb_params.Common.guestinfo.ntp.Value = $b[12]

Import-VApp -VMHost $b[3] -Source $b[4] -Name $b[5] -OvfConfiguration $cb_params -Force 
Start-VM -VM $b[5]
