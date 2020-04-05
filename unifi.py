#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import logging
import json
import sys

logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('log/app.log')
sh = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[%(asctime)s] - %(filename)s[%(lineno)d] - %(funcName)s - %(message)s',
                               datefmt='%a, %d %b %Y %H:%M:%S')
fh.setFormatter(formatter)
sh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(sh)

class unifi(object):
	""" Осуществляет перезапуск точек доступа, подключенных к Unifi Controller средствами Unifi API """
	def __init__(self, api_url, api_username, api_password, api_site = 'default'):
		super(unifi, self).__init__()
		self.__api_url = api_url
		self.__api_username = api_username
		self.__api_password = api_password
		self.__api_site = api_site
		self.content_type = 'application/json'
		self.api_login_url = "/api/login"
		self.api_logout_url = "/api/logout"
		self.api_devices_url = "/stat/device-basic"
		self.api_devmgr_url = "/cmd/devmgr"
		if self.__login() == False:
			sys.exit()
		
	''' Возвращает json с заголовками для авторизации '''
	def __get_headers(self):
		headers = {
			'Content-Type': self.content_type,
		}
		return headers

	''' Возвращает json с данными для авторизации '''
	def __get_login_data(self):
		data = {
			"username": self.__api_username,
			"password": self.__api_password
		}
		return json.dumps(data)

	''' Полный url для авторизации '''
	def __get_login_url(self):
		url = self.__api_url + self.api_login_url
		return url

	''' Полный url для получения списка подключенных устройств '''
	def __get_devices_url(self):
		url = self.__api_url + '/api/s/' + self.__api_site + self.api_devices_url
		return url

	''' Полный url для перезагрузки подключенного устройства '''
	def __get_restart_device_url(self):
		url = self.__api_url + '/api/s/' + self.__api_site + self.api_devmgr_url
		return url

	''' Возвращает json с данными для перезапуска устройства '''
	def __get_restart_device_data(self, mac):
		data = {
			"cmd": "restart",
			"mac": mac
		}
		return json.dumps(data)

	''' Авторизация на UnifiController '''
	def __login(self):
		login_url = self.__get_login_url()
		headers = self.__get_headers()
		login_data = self.__get_login_data()
		logging.info( u'Отправка запроса авторизации')
		unifi = requests.request("POST", login_url, data=login_data, headers=headers, verify=False)
		login_result = json.loads(unifi.text)
		if login_result['meta']['rc'] == 'error':
			logging.error( u'Ошибка авторизации. Ответ API: ' + login_result['meta']['msg'])
			return False
		else:
			logging.info( u'Авторизация успешна')
			self.cookies = unifi.cookies
			return True

	''' Возвращает список устройств, подключенных к контроллеру '''
	def __get_devices_list(self):
		devices_list_url = self.__get_devices_url()
		devices_headers = self.__get_headers()
		logging.info( u'Запрос списка устройств, подключенных к контроллеру')
		devices = requests.get(devices_list_url, headers=devices_headers, verify=False, cookies=self.cookies)
		devices_list = json.loads(devices.text)
		if devices_list['data'] is None:
			logging.error( u'Отсутствует возможность получить список устройств')
			sys.exit()
		else:
			logging.info( u'Список устройств получен')
			return devices_list['data']

	''' Перезагружает устройство, подключенное к Unifi Controller по mac-адресу '''
	def __restart_device(self, mac):
		device_restart_url = self.__get_restart_device_url()
		device_restart_data = self.__get_restart_device_data(mac)
		headers = self.__get_headers()
		logging.info( u'Попытка перезагрузки устройтва')
		device_restart = requests.request("POST", device_restart_url, data=device_restart_data, headers=headers, verify=False, cookies=self.cookies)
		logging.info( u'Устройство перезагружено')
		return json.loads(device_restart.text)

	''' Перезагружает все подключенные к контроллеру устройства '''
	def restart_all_devices(self):
		lists = self.__get_devices_list()
		for device in lists:
			mac = device.get('mac')
			logging.info( u'Перезагрузка устройтва ' + mac)
			self.__restart_device(mac)

	''' Производит отключение от контроллера '''
	def __disconnect(self):
		pass
