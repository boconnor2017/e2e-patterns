# Builds the master controller
# Author: Brendan O'Connor
# Date: August 2023

python3 -m ensurepip
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade pip setuptools
python3 -m pip install flask-restful
python3 wrapper-build-e2e-pattern-mc.py
