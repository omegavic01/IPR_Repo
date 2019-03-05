#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#
#

import os
import urllib3
import infoblox_netmri
import logging
from dotenv import find_dotenv, load_dotenv
#
# We are using a cert that this box does not know about
# This disable trust warnings
#

urllib3.disable_warnings()


def main():
    host = PAYLOAD['host']
    username = PAYLOAD['username']
    password = PAYLOAD['password']
    #use_ssl = os.environ['NETM_USE_SSL']
    api_version = PAYLOAD['api_version']
    #ssl_verify = os.environ.get['NETM_SSL_VERIFY']

    c = infoblox_netmri.InfobloxNetMRI(
        host=host,
        username=username,
        password=password,
        api_version=api_version) #,
       # use_ssl=use_ssl,
       # ssl_verify=ssl_verify)

    print(c)

    devices = c.api_request('devices/index',{'timeout': 10, 'limit': 3000})

    #FORMAT='%16s %80s'
    #print FORMAT % ('DeviceName', ' running_config_text')
    #
    for d in devices['devices']:
    #  print FORMAT % (d['DeviceName'], d['running_config_text'])
        save_path = '/my/custom/path'
        tgt_file = '{}.cfg'.format(d['DeviceName'])
        full_path_file = os.path.join(save_path, tgt_file)
        with open(full_path_file, 'w+') as f1:
            f1.writelines(d['running_config_text'])


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
    main()