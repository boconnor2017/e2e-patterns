#!/bin/sh
param(
[string]$a
)
$b = $a.Split(" ")
Set-PowerCLIConfiguration -Scope User -ParticipateInCEIP $true
Connect-VIServer -Server $b[0] -Protocol https -User $b[1] -Password $b[2] -Force
Start-VM -Name $b[3] -Confirm:$false
