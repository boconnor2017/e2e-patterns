# Welcome to E2E Patterns
![alt text](https://github.com/boconnor2017/e2e-patterns/blob/main/img/E2E-Patterns-Logo-01.png)
This repository is intended to provide code samples to help you build immutable VMware Patterns. See the Wiki for details.

:heavy_exclamation_mark: ***WARNING: the contents of this repository are not intended for production networks in their current state. It is recommended that these scripts are certified in a Development environment, functionally tested, and refactored with the appropriate security and operational considerations. Proper SDLC practices are advised.***

# What is a Pattern?
Think of a "Pattern" like a Docker Image. A Docker Image might be very generic or it might be fully baked with specific packages. Similarly, a Pattern is a set of packages (from this repo) designed to function on a PhotonOS virtual machine. The result of a Pattern (a Docker Container using the Docker analogy) is the VMware environment that the Pattern creates. For example: a Workload Domain Pattern might consist of a vCenter Server, an NSX Manager, and a few nested ESXi hosts. The Pattern in this example would contain all code from this repo to automate the build of a workload domain, formatted to run on PhotonOS. 

# Pattern Types
* Basic PhotonOS Patterns: provide basic tools such as an OVFTool container, a PowerCLI container, a Terraform container, and a Minikube environment.
* Shared Services Patterns: provide standard shared services tools such as a DNS container, an LDAP container, and NFS container.
* Workload Domain Patterns: provide VMware nested capabilities such as vCenter, NSX, Aria, and Tanzu.

# Architecture 
* Environment: the available physical resources (compute, network, and storage) used to host Photon appliances and Patterns.
* Master Controller: the primary photon appliance used to run all Patterns.
* Pattern Controller: secondary photon appliances used to store necessary binaries and to run necessary scripts for the Pattern.

Each PhotonOS appliances (i.e. the Master Controller and the Pattern Controllers) are enabled with the following RPMs by default:
* Docker
* Bindutils
* Git
* Python

All Patterns are built using Python 3. Each PhotonOS appliances (i.e. the Master Controller and the Pattern Controllers) are enabled with the following Python modules by default (via Pip):
* flask-restful
* docker
* paramiko
* vsphere-automation-sdk-python

# Documentation
https://github.com/boconnor2017/e2e-patterns/wiki
