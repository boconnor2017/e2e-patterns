# Welcome to the E2E Patterns Lab
The purpose of this lab is to demo or experiment with VMware technologies (such as vSphere) or VMware concepts (such as Docker or Kubernetes) using a series of automated, zero-touch labs. All code in this repository is tested regularly and updated based on relevant field use cases (such as demos or training). All labs are standardized to run on PhotonOS.

❗ WARNING: the contents of this wiki are not intended for production networks. In most cases, best practices for operational compliance are not followed. The intended use of this wiki is for home labs only.

# Quick Start
For a detailed documentation of this lab please see the wiki page: https://github.com/boconnor2017/e2e-k8-lab/wiki

## Step 1: Deploy Photon (photon-ova-4.0-ca7c9e9330.ova)
For downloads visit: https://github.com/vmware/photon/wiki/Downloading-Photon-OS 

The default password is `changeme`. For all labs, use `/usr/local/` as the working directory.
```
cd /usr/local/
```

## Step 2: Download controller prep script 
```
curl https://raw.githubusercontent.com/boconnor2017/e2e-k8-lab/main/prep-photon.sh >> prep-photon.sh
```

## Step 3: Download refresher script
```
curl https://raw.githubusercontent.com/boconnor2017/e2e-k8-lab/main/refresh-e2e-k8-lab.sh >> refresh-e2e-k8-lab.sh
```

## Step 4: Run E2E lab PhotonOS prep script
```
sh prep-photon.sh
```

## Step 5: Refresh local repo (as needed)
```
sh refresh-e2e-k8-lab.sh
```

# Labs
See table of contents in the wiki: https://github.com/boconnor2017/e2e-k8-lab/wiki/Table-of-Contents

