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


