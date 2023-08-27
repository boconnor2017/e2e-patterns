# Configures Photon using PowerCLI container
# Author: Brendan O'Connor
# Date: August 2023
docker run --rm --entrypoint="/usr/bin/pwsh" -v ${PWD}:/tmp vmware/powerclicore /tmp/wrapper-configure-e2e-pattern.ps1 "172.16.0.201 root VMware1!"
