# E2E Patterns Python Library 2024
# Author: Brendan O'Connor
# Date: January 2024
# Version: 3.0
# Reference: https://github.com/boconnor2017/e2e-patterns

import requests
import urllib3
import urllib
import shutil
import time
import json
import os
import docker 
import paramiko
import docker
import subprocess
import sys
from vmware.vapi.vsphere.client import create_vsphere_client
from datetime import datetime
import config

def download_file_from_github(url, filename):
    urllib.request.urlretrieve(url, filename)

def e2e_patterns_header(logfile_name, pattern_name):
    err = ""
    write_to_logs(err, logfile_name)
    err = "-----------------------------------------------------"
    write_to_logs(err, logfile_name)
    err = "-----------------------------------------------------"
    write_to_logs(err, logfile_name)
    err = "-----------------------------------------------------"
    write_to_logs(err, logfile_name)
    err = "WELCOME TO E2E PATTERNS 2024!"
    write_to_logs(err, logfile_name)
    err = "-----------------------------------------------------"
    write_to_logs(err, logfile_name)
    err = "-----------------------------------------------------"
    write_to_logs(err, logfile_name)
    err = "-----------------------------------------------------"
    write_to_logs(err, logfile_name)
    err = "Starting build of pattern "+pattern_name
    write_to_logs(err, logfile_name)
    err = "Author: Brendan O'Connor"
    write_to_logs(err, logfile_name)
    err = ""
    write_to_logs(err, logfile_name)

def write_to_logs(err, logfile_name):
    tstamp = str(datetime.now())
    logfile = open(logfile_name, "a")
    logfile.write(tstamp+": "+err+" \n")
    logfile.close
