python3 -m ensurepip
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade pip setuptools
curl -L https://bootstrap.saltstack.com -o install_salt.sh
sh install_salt.sh -A <Salt Master IP address>
