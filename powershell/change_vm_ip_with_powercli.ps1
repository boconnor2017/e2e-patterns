# PowerCLI Script to change the IP address of a virtual machine
# Author: Brendan O'Connor
# Date: August 2023

# Capture input from command line 
# 0: ESXi Host 
# 1: ESXi User (root recommended)
# 2: ESXi Password
# 3: VM Name
# 4: New IP Address
# 5. New Subnet Mask
# 6. New Default Gateway 
#

param(
[string]$a
)

# Parse Command Line Inputs
$b = $a.Split(" ")

# Change IP commands
$chg_ip_cmd = "ifconfig eth0 "+$b[4]+" netmask "+$b[5]
$chg_df_gw = "route add default gateway  "+$b[6]

# Connect to ESXi Host
Connect-VIServer -Server $b[0] -Protocol https -User $b[1] -Password $b[2] -Force

# Configure IP Address
Set-VMKeystrokes -VM $b[3] -Stringinput $chg_ip_cmd -ReturnCarriage $true -DebugOn $false | Out-Null
Start-Sleep -Seconds 1.5
Set-VMKeystrokes -VM $b[3] -Stringinput $chg_df_gw -ReturnCarriage $true -DebugOn $false | Out-Null
Start-Sleep -Seconds 1.5
