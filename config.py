#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser

class config(object):
	""" Возвращает параметры конфигурации """
	def __init__(self, configfile = 'config/config.ini'):
		super(config, self).__init__()
		self.config = configparser.ConfigParser()
		self.config.read(configfile)

	''' Возвращает url UnifiController '''
	def get_unifi_url(self):
		return self.config.get('UNIFI', 'url')

	''' Возвращает имя пользователя UnifiController из файла конфигурации '''
	def get_unifi_username(self):
		return self.config.get('UNIFI', 'username')

	''' Возвращает пароль пользователя UnifiController из файла конфигурации '''
	def get_unifi_password(self):
		return self.config.get('UNIFI', 'password')