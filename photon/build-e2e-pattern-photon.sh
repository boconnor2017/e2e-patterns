Builds a PhotonOS VM
# Author: Brendan O'Connor
# Date: August 2023

python3 -m ensurepip
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade pip setuptools
python3 -m pip install --upgrade git+https://github.com/vmware/vsphere-automation-sdk-python.git
python3 -m pip install docker
python3 wrapper-build-e2e-pattern-photon.py $1 $2
