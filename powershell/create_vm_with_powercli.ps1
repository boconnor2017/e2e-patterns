#!/bin/sh
param(
[string]$a
)
$b = $a.Split(" ")
Set-PowerCLIConfiguration -Scope User -ParticipateInCEIP $true
Connect-VIServer -Server b[1] -Protocol https -User b[2] -Password b[3] -Force
New-VM -Name b[4]
