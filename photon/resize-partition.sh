#!/bin/bash
# Description: Scans and resizes partition for Photon Controller
# Author: Brendan O'Connor
# Date: February 2024
# Version: 1.0
# Rescan Storage
echo 1 > /sys/class/block/sda/device/rescan
# fdisk shell
fdisk /dev/sda <<EEOF
d
2
n
2
30720

w
EEOF
exit 0
