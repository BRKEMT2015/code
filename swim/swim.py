#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Port utilisation code for many switches
Copyright (c) 2021 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""


__author__ = "Christina Skoglund"
__email__ = "cskoglun@cisco.com"
__copyright__ = "Copyright (c) 2021 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

import requests
import json
import pandas as pd
import urllib3
urllib3.disable_warnings() ### NOT ADVISED TO USE DISABLE WARNINGS IN PRODUCTION ENVIRONMENT

### Creating function to retrieve token
def get_dnac_token():
	url_token = "https://sandboxdnac.cisco.com/dna/system/api/v1/auth/token" #Change URL for your environment if you want

	payload = {}
	headers = {
	  'Content-Type': 'application/json',
	  'Authorization': 'Basic ZGV2bmV0dXNlcjpDaXNjbzEyMyE='
	}

	response = requests.request("POST", url_token, headers=headers, data = payload, verify=False) #REST API request
	response = response.json() #Parse JSON into Python dictionary
	token = response['Token'] #Find token value in response data
	return token

### Creating function to retrieve device list data
def get_network_device_list():
	url_networkdevices = "https://sandboxdnac.cisco.com/dna/intent/api/v1/network-device"

	payload = {}
	headers = {
	  'Content-Type': 'application/json',
	  'X-Auth-Token': get_dnac_token() # Calling for the function that retrieves the token (see above)
	}

	response = requests.request("GET", url_networkdevices, headers=headers, data = payload,verify=False) #REST API request
	device_list = response.json() #Parse JSON into Python dictionary
	return device_list #Return device list data


### From here on we try to identify the data points we want to export to an Excel document called document.xlsx
device_data = get_network_device_list()

serialnr_list = []
swVersion_list = []

### Loop through the data set and identify the data points to export and save them in two separate lists
for item in device_data['response']:
	serialnr_list.append(item['serialNumber'])
	swVersion_list.append(item['softwareVersion'])

### Use the Pandas library to create a data frame with these lists in order to export them
df = pd.DataFrame({'serialNr':serialnr_list,
'softwareVersion':swVersion_list})
df.to_excel('document.xlsx', index = False)


