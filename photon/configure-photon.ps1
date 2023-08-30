# PowerCLI Script to configure PhotonOS
# Author: Brendan O'Connor
# Date: August 2023

# Capture input from command line 
# 0: ESXi Host 
# 1: ESXi User (root recommended)
# 2: ESXi Password
# 3: PhotonOS VM Name
# 4: PhotonOS New Guest Password 
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

# Configure new password
Set-VMKeystrokes -VM $b[3] -Stringinput "root" -ReturnCarriage $true -DebugOn $false | Out-Null
Set-VMKeystrokes -VM $b[3] -Stringinput "changeme" -ReturnCarriage $true -DebugOn $false | Out-Null
Set-VMKeystrokes -VM $b[3] -Stringinput "changeme" -ReturnCarriage $true -DebugOn $false | Out-Null
Set-VMKeystrokes -VM $b[3] -Stringinput $b[4] -ReturnCarriage $true -DebugOn $false | Out-Null
Set-VMKeystrokes -VM $b[3] -Stringinput $b[4] -ReturnCarriage $true -DebugOn $false | Out-Null
