#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import requests
import sys
from unifi import unifi
from config import config
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

"""
Написать README.md
"""

conf = config()
url = conf.get_unifi_url()
username = conf.get_unifi_username()
password = conf.get_unifi_password()

if __name__ == '__main__':
	unifi = unifi(url, username, password)
	unifi.restart_all_devices()
