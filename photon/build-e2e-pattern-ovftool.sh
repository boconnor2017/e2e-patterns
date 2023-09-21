# Description: Build OVFTool Docker Container
# Author: Brendan O'Connor
# Date: August 2023
# Version: 1.0
cp /usr/local/drop/VMware-ovftool* $PWD
docker build -t ovftool .
