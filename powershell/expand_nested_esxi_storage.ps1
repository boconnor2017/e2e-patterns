#!/bin/sh
# PowerCLI Script to expand storage for nested ESXi host (vCenter required)
# Author: Brendan O'Connor
# Date: February 2024
# Version: 1.0

# Capture input from command line 
# 00: vCenter Server
# 01: vCenter User (administrator@vsphere.local recommended)
# 02: vCenter Password
# 03: Name of Nested ESXi virtual machine that you are expanding  
# 04: Capacity (GB) to expand to (number) 

param(
[string]$a
)

# Parse Command Line Inputs
$b = $a.Split(" ")

# Connect to vCenter
Connect-VIServer -Server $b[0] -Protocol https -User $b[1] -Password $b[2] -Force

# Expand Nested ESXi Disk Capacity
$disks = Get-HardDisk -VM $b[3]
Set-HardDisk -HardDisk $disks[2] -CapacityGB $b[4] -Confirm:$false
Restart-VM -VM $b[3] -Confirm:$false
