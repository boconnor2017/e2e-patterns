# PowerCLI Script to attach an ISO to virtual machine
# Author: Brendan O'Connor
# Date: January 2024

# Capture input from command line 
# 0: ESXi Host 
# 1: ESXi User (root recommended)
# 2: ESXi Password
# 3: VM Name
# 4: Datastore Name 
# 5: Path and filename (syntax: folder\VMware-VCSA-x.iso)
#
# Syntax: docker run --rm --entrypoint="/usr/bin/pwsh" -v ${PWD}:/tmp vmware/powerclicore /tmp/test.ps1 '172.16.0.201 root VMware1! e2ep-photontest-09 VMware1!VMware1!'

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

# Attach ISO to datastore
$cddvddrive = Get-CDDrive -VM $b[3] 
$datastore = $b[4]
$pathtoiso = $b[5]

Set-CDDrive -CD $cddvddrive -IsoPath "[$datastore] $pathtoiso" -Connected:$true -StartConnected:$true -Confirm:$false
