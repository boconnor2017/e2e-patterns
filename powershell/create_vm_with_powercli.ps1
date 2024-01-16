#!/bin/sh
param(
[string]$a
)
$b = $a.Split(" ")
Connect-VIServer -Server b[1] -Protocol https -User b[2] -Password b[3] -Force
New-VM -Name THISWORKS
