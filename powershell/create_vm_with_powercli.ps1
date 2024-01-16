#!/bin/sh
Connect-VIServer -Server 172.16.0.201 -Protocol https -User root -Password VMware1! -Force
New-VM -Name THISWORKS
