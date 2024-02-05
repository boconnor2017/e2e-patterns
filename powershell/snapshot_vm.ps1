#!/bin/sh
# PowerCLI Script to snapshot a virtual machine
# Author: Brendan O'Connor
# Date: February 2024
# Version: 1.0

# Capture input from command line 
# 00: vCenter Server
# 01: vCenter User (administrator@vsphere.local recommended)
# 02: vCenter Password
# 03: Name of virtual machine that you are creating a snapshot for 
# 04: Name of the snapshot 

param(
[string]$a
)

# Parse Command Line Inputs
$b = $a.Split(" ")

# Connect to vCenter
Connect-VIServer -Server $b[0] -Protocol https -User $b[1] -Password $b[2] -Force
New-Snapshot -VM $b[3] -Name $b[4]
