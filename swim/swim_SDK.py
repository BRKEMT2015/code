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





