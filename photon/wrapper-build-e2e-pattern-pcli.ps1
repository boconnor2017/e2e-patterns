# PowerCLI Script to configure PhotonOS
# Author: Brendan O'Connor
# Date: August 2023

# Capture input from command line 
# 0: ESXi Host 
# 1: ESXi User (root recommended)
# 2: ESXi Password
# 3: PhotonOS Guest User (root recommended)
# 4: PhotonOS Guest Password 
param(
[string]$a
)

# Parse Command Line Inputs
$b = $a.Split(" ")

# Connect to ESXi Host
Connect-VIServer -Server $b[0] -Protocol https -User $b[1] -Password $b[2] -Force
$vm_list = Get-VM
$vm_config_script = "mkdir /usr/local/TEST"
foreach($vm in $vm_list){
	Get-VMGuest -VM $vm
	Invoke-VMScript -VM $vm -ScriptText $vm_config_script -GuestUser $b[3] -GuestPassword $b[4]
}
