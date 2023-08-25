# Build files should follow this naming convention: build-e2e-pattern-<NAME>.sh
# Copy Template Below
# # # # # # # # # # # # # # # # # # # # # # # # #
# <DESCRIPTION>
# Author: Brendan O'Connor
# Date: <MONTH YEAR>

python3 -m ensurepip
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade pip setuptools
# Add necessary pip packages (example below)
python3 -m pip install flask-restful
# Add these when you need to use the vSphere Python SDK
python3 -m pip install --upgrade pip setuptools
python3 -m pip install --upgrade git+https://github.com/vmware/vsphere-automation-sdk-python.git
# Call wrapper (example below)
python3 wrapper.py
