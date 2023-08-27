# Configures Photon using PowerCLI container
# Author: Brendan O'Connor
# Date: August 2023
docker run --rm --entrypoint="/usr/bin/pwsh" -v ${PWD}:/tmp vmware/powerclicore /tmp/wrapper-configure-e2e-pattern-photon.ps1 "$1 $2 $3 $4 $5"
