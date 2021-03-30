# USE CASE 2: Are all the network switvhes in correct software version?

![alt text](/images/swim.png "Software Image check use case")

In this use case Antti needs to check the software version that each of his devices in his network are running, to ensure that they are running on a safe version. This time however, Antti will programming against a controller, Cisco DNA Center, and leverage the already collected and structured data of the devices that DNA Center has to offer. 

## Getting Started
- Make sure you have installed the requirements.txt to have all the required libraries in your development environment
- Select which Cisco DNA Center you want to work with. Good option is to work with the Cisco DNA Center sandbox in the [DevNet Sandbox](https://devnetsandbox.cisco.com/)

## Using POSTMAN with Cisco DNA Center APIs

First thing that we should do when learning to use a new API is to test it to see how it works and what kind of response we get. [Postman](https://www.postman.com/) is a great tool for this! Lets see how we would navigate and find the correct REST APIs of DNA Center to work with.

In order to be able to work with the Cisco DNA Center APIs, Antti needs to use an Authentication Token. This token is retrieved by using the Authentication API. Tha is where Antti will start. 

1. Lets use this in Postman as the request url in order to retrieve the Authentication Token:
![alt text](images/postman_dnac_auth_url.png "Postman Authentication URL")
Notice that we are posting information, therefor the method should be **POST**.
Please note that you should use your Cisco DNA Center URL or IP address in the place of {{baseurl}}. 

2. In order to receive the Authentication Token, Antti will need to get proper authorization by the controller. 
![alt text](images/postman_dnac_auth.png "Postman DNA Center credentials")
We use *basic auth* for the authorization with the Cisco DNA Center username and password. Please note that you should put in the place of {{user}} your switch username and in the place of {{password}} your switch password.

3. After the previous sections are filled, we can send our request, and will receive an response:
![alt text](images/postman_dnac_token.png "Postman DNA Center Token Retrieved")
Note how the status is 200 OK, meaning that our request was successful. We have gotten the token in JSON format. 

4. Now we need to retrieve device information by using the Device List API. 
![alt text](images/postman_dnac_getdevicesurl.png "Postman Device List REST API")
Just as in step 1, we add the url of the API but this time we will retrieve data, therefore the method should be **GET**.
Please note that you should use your Cisco DNA Center URL or IP address in the place of {{baseurl}}. 

5.
![alt text](images/postman_dnac_headers.png "Postman Headers")
Note how we are using the token that we retrieved in step 1-3, in order to make this REST API call to the Cisco DNA Center. 

6.
![alt text](images/postman_dnac_json.png "Postman Device List Data in JSON Format")
Note how the status is 200 OK, meaning that our request was successful. We have gotten the token in JSON format. 

## A script to verify the software version of the network devices

TBD


## A script utilising Cisco DNA Center SDK

TBD
