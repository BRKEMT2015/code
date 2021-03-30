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

from dnacentersdk import api
import pandas as pd

### Simplify authentication with dnacentersdk
dnac = api.DNACenterAPI(username=USERNAME_DNAC, 
	    	          password=PASSWORD_DNAC,
    		          base_url=sandboxdnac2.cisco.com:443 ,
		          verify=False)

### Get Device List
device_list = dnac.devices.get_device_list()

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





