# PowerCLI Script to capture list of virtual machines on an ESXi host
# Author: Brendan O'Connor
# Date: January 2024

# Capture input from command line 
# 0: ESXi Host 
# 1: ESXi User (root recommended)
# 2: ESXi Password

param(
[string]$a
)

# Parse Command Line Inputs
$b = $a.Split(" ")

# Connect to ESXi Host
Connect-VIServer -Server $b[0] -Protocol https -User $b[1] -Password $b[2] -Force

$vmlist = Get-VM | Select Name 
Write-Host $vmlist  
