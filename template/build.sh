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
# Call wrapper (example below)
python3 wrapper-build-e2e-pattern-mc.py
