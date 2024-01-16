#!/bin/sh
param(
[string]$a
)
$b = $a.Split(" ")
Connect-VIServer -Server $b[0] -Protocol https -User $b[1] -Password $b[2] -Force
Start-VM -VM $b[3] -Confirm:$false
