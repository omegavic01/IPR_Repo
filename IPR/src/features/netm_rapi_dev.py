#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import os
import logging
from dotenv import find_dotenv, load_dotenv


def main(project_dir):
    # get logger
    logger = logging.getLogger(__name__)
    logger.info('Beginning of Script')
    raw_data_path = os.path.join(project_dir, 'data', 'raw')
    devices_data_path = os.path.join(raw_data_path, 'devices.pkl')
    url = "https://"
    # Lists every device name within NetMRI
    # object_type = "/api/" + PAYLOAD['api_version'] + "/devices/index"

    # Lists every device name within NetMRI (Could not get to work!)
    object_type = "/api/" + PAYLOAD['api_version'] + "/devices/search?" \
                                                     "DeviceName ne 'unknown'"

    # Worked but NetMRI version of VLANID is required.
    # object_type = "/api/" + PAYLOAD['api_version'] + \
    #               "/vlan_members/search?VlanID=723069&include=device,interface"

    # Dict with Vlan ID and a bunch of STP information
    # object_type = "/api/" + PAYLOAD['api_version'] + "/vlan_members"

    # Dict with the actual Vlan number and Vlan ID used by Netmri.
    # object_type = "/api/" + PAYLOAD['api_version'] + \
    #               "/device_by_vlanname_or_vlanindex_grids/index"
    data = requests.get(url + PAYLOAD['host'] + object_type, verify=False,
                        auth=(PAYLOAD['username'], PAYLOAD['password']))

    json_input = data.text

    # Remember to change the dict value!!!!  devices, vlan_members etc.
    try:
        decoded = json.loads(json_input)
        for entry in decoded['vlan_members'][1]:
            print(entry)

    except (ValueError, KeyError, TypeError):
        print("JSON format error")


if __name__ == '__main__':
    # getting root directory
    PROJECT_DIR = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

    # setup logger
    LOG_FMT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=LOG_FMT)

    # find .env automatically by walking up directories until it's found
    DOTENV_PATH = find_dotenv()

    # load up the entries as environment variables
    load_dotenv(DOTENV_PATH)

    # PAYLOAD for login to IPAM
    PAYLOAD = {
        'host': os.environ.get("NETM_HOST"),
        'username': os.environ.get("NETM_USERNAME"),
        'password': os.environ.get("NETM_PASSWORD"),
        'api_version': os.environ.get("NETM_API_VERSION")
    }

    # call the main
    main(PROJECT_DIR)
