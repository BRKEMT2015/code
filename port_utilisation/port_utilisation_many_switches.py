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

import requests
import csv

# disable insecure request warnings in terminal
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"
__copyright__ = "Copyright (c) 2021 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

def get_switch_credentials(csv_file):
    '''
    Function to get network switch credentials from a CSV file. These
    credentials will be used when we connect to the switches via RESTCONF.
    CSV file should include the IP address, username and password using the
    following keys: IP, USER, PW
    E.g.
    IP,USER,PW
    10.10.10.1,admin,myPassw0rd
    10.10.10.2,admin,myPassw0rd
    10.10.10.3,admin,myPassw0rd

    Function arguments:
    - a string of the csv filename

    Returns:
    - credentials from the csv_file as a list of dictionaries
    '''

    credentials = []

    with open(csv_file, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            credentials.append(row)
    return credentials

def get_switch_if_utilisation(ip, username, password, rc_port=443):
    '''
    Function to get number of up and down interfaces for a switch. Will require the ip address,
    username and password for the switch in order to create RESTCONF connection.
    In the returned response we have the key "Cisco-IOS-XE-interfaces-oper:interface"
    that includes a list of all the interfaces on the switch. The key "oper-status" provides
    the status for each interface, with which we can check how many ports are up and how many down.

    Function arguments:
    - A string of switch ip address
    - A string of switch username
    - A string of switch password
    - Optionally integer for restconf port, if it is not the default one

    Returns:
    - dictionary with number of up and down interfaces, to be accessed with keys "up" and "down"
    '''

    print("Connecting to switch {}".format(ip))
    url = "https://{}:{}/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces/interface".format(ip, rc_port)

    header = {
        "content-type": "application/yang-data+json",
        "accept": "application/yang-data+json"
    }
    response= requests.get(url, auth=(username, password), headers=header, verify=False)
    interfaces = response.json()["Cisco-IOS-XE-interfaces-oper:interface"]

    switch_utilisation = {"up": 0, "down": 0}
    for interface in interfaces:
        if interface["interface-type"] == "iana-iftype-ethernet-csmacd":
            status = interface["oper-status"]
            if status == "if-oper-state-ready":
                switch_utilisation["up"] += 1
            elif status == "if-oper-state-lower-layer-down" or status == "if-oper-state-no-pass":
                switch_utilisation["down"] += 1

    print("{} ports: {} up, {} down".format(ip, switch_utilisation["up"], switch_utilisation["down"]))

    return switch_utilisation

def main():
    '''
    Main function that calls the previously defined functions.
    We get the credentials of our switches, and get port utilisation information for all
    of them. Finally we print out the port utilisation percentage and the number of ports
    that are up or down in the network.
    '''
    
    summary = {
        "total_up": 0,
        "total_down": 0
    }

    credentials = get_switch_credentials("credentials.csv")
    for switch in credentials:
        switch_utilisation = get_switch_if_utilisation(switch["IP"], switch["USER"], switch["PW"])
        summary["total_up"] += switch_utilisation["up"]
        summary["total_down"] += switch_utilisation["down"]

    port_utilisation = summary["total_up"]/(summary["total_up"]+summary["total_down"])
    port_utilisation = round(port_utilisation, 2)
    print("\nTotal port utilisation in the network: {}".format(port_utilisation))
    print("Up: {}".format(summary["total_up"]))
    print("Down: {}".format(summary["total_down"]))

if __name__ == "__main__":
    main()