# E2E Patterns Photon Prep Script
# Author: Brendan O'Connor
# Date: September 2023

# Update/install basic Linux tools
yum -y update
yum -y install git bindutils
yum -y install https://repo.ius.io/ius-release-el$(rpm -E '%{rhel}').rpm
# Install python3
yum -y install python3
python3 --version
# Create drop folder
mkdir /usr/local/drop
# Clone this repository
git clone https://github.com/boconnor2017/e2e-patterns.git /usr/local/e2e-patterns
# Start Docker
systemctl start docker
systemctl status docker
# Configure DNS to ensure public nslookup
curl https://raw.githubusercontent.com/boconnor2017/e2e-patterns/main/dns/resolv.conf >> /run/systemd/resolve/new-resolv.conf
rm /run/systemd/resolve/stub-resolv.conf
rm /etc/resolv.conf
cp /run/systemd/resolve/new-resolv.conf /run/systemd/resolve/stub-resolv.conf
cp /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf
#systemctl restart systemd-resolved.service
# Pause 10 seconds before running pip commands
sleep 10
# Run necessary pip commands
python3 -m ensurepip
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade pip setuptools
python3 -m pip install flask-restful
python3 -m pip install docker
python3 -m pip install paramiko
# Add vSphere Python SDK
python3 -m pip install --upgrade pip setuptools
python3 -m pip install --upgrade git+https://github.com/vmware/vsphere-automation-sdk-python.git
