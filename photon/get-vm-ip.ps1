# PowerCLI Script to get IP address of a VM
# Author: Brendan O'Connor
# Date: August 2023

# Capture input from command line 
# 0: ESXi Host 
# 1: ESXi User (root recommended)
# 2: ESXi Password
# 3: VM Name
#
# Syntax: docker run --rm --entrypoint="/usr/bin/pwsh" -v ${PWD}:/tmp vmware/powerclicore /tmp/test.ps1 '172.16.0.201 root VMware1! e2ep-photontest-12'

param(
[string]$a
)

# Parse Command Line Inputs
$b = $a.Split(" ")
foreach($args in $b){
	Write-Host $args
}

# Connect to ESXi Host
Connect-VIServer -Server $b[0] -Protocol https -User $b[1] -Password $b[2] -Force

# Return IP address
(Get-VM -Name $b[3]).Guest.IPAddress[0]
