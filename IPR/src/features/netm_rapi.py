#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import os
import logging
from dotenv import find_dotenv, load_dotenv
import pickle


def api_devices(path):
    total = 0
    url = "https://"

    def api_call(limit):
        if limit == 0:
            object_type = "/api/" + PAYLOAD['api_version'] + "/devices/index"
            data = requests.get(url + PAYLOAD['host'] + object_type,
                                verify=False,
                                auth=(
                                PAYLOAD['username'], PAYLOAD['password']))
        if limit != 0:
            object_type = "/api/" + PAYLOAD['api_version'] + \
                          "/devices/index?limit=" + str(limit)
            data = requests.get(url + PAYLOAD['host'] + object_type,
                                verify=False, auth=(PAYLOAD['username'],
                                                    PAYLOAD['password']))
        return json.loads(data.text)

    device_data = api_call(total)
    if 1000 < device_data['total'] <= 10000:
        device_data = api_call(str(device_data['total'] + 200))
    pickle.dump(device_data, open(path, "wb"))


def main(project_dir):
    """Script built to make api call's for Data used later on by other scripts.
    """
    # get logger
    logger = logging.getLogger(__name__)
    logger.info('Beginning of Script')
    raw_data_path = os.path.join(project_dir, 'data', 'raw')
    devices_data_path = os.path.join(raw_data_path, 'devices.pkl')

    api_devices(devices_data_path)


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
