# Quick Start
❗ WARNING: the contents of this wiki are not intended for production networks. In most cases, best practices for operational compliance are not followed. The intended use of this wiki is for home labs only. For a detailed documentation of this lab please see the wiki page: https://tinyurl.com/e2e-patterns

## Step 1: Deploy Photon (photon-ova-4.0-ca7c9e9330.ova)
For downloads visit: https://github.com/vmware/photon/wiki/Downloading-Photon-OS 

The default password is `changeme`. For all labs, use `/usr/local/` as the working directory.
```
cd /usr/local/
```

## Step 2: Download controller prep script 
```
curl https://raw.githubusercontent.com/boconnor2017/e2e-patterns/main/prep-photon.sh >> prep-photon.sh
```

## Step 3: Download refresher script
```
curl https://raw.githubusercontent.com/boconnor2017/e2e-patterns/main/refresh-e2e-patterns.sh >> refresh-e2e-patterns.sh
```

## Step 4: Run E2E lab PhotonOS prep script
```
sh prep-photon.sh
```

## Step 5: Refresh local repo (as needed)
```
sh refresh-e2e-patterns.sh
```

# Labs
See table of contents in the wiki: https://tinyurl.com/e2e-patterns-toc

