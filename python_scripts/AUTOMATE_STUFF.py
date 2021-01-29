import netmiko
import datetime
import os
import json
import gnupg
import concurrent.futures
import time


#Set gnupg home
gpg = gnupg.GPG(gnupghome=f'{os.getcwd()}/gnupg')

#Get encrypted json file and decrypt for use.
with open('device_creds.json', 'rb') as jfile:
    data = json.load(jfile)

