from __future__ import absolute_import, unicode_literals
import praw
import json 
import os 
import io

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class apiBackend(object):

	def __init__(self,mode=None,auth_uri=None, user=None):
		self.mode=mode
		self.auth_uri=auth_uri
		self.user=user
	
	def load_config(self):
		DEFAULT_CONFIG = None
		loaded_config = os.environ.get('WCSRL_CONFIG_FILE', DEFAULT_CONFIG)
		if loaded_config is None:
			print('We need a config to make this work!\n')
			exit(1)
	
		else:
			with io.open(loaded_config, mode='r', encoding='utf8') as config:
				self.config = json.loads(config.read())
				return self.config

	def get_roauth_url(self):
		if self.auth_uri is None:
			try:
				self.reddit = praw.Reddit(
					client_id = self.config['reddit']['id'],
					client_secret = self.config['reddit']['secret'],
					user_agent = self.config['reddit']['user_agent'],
					redirect_uri = self.config['reddit']['redirect_uri']
				)
				self.auth_uri = self.reddit.auth.url(['identity', 'history'], state='idkwtfid', duration='temporary')
				return self.auth_uri

			except Exception as exc:
				print('{0} - Unable to auth to reddit, check your creds'.format(exc))	
				exit(0)
		else:
			return self.auth_uri

	def set_user(self, token):
		if self.user is None:
			self.reddit.auth.authorize(token)
			self.user = self.reddit.user.me()
			print(self.user)
			return self.user
		else:
			 return self.user

	def get_links(self):
		self.links = ''
		for link in self.user.saved(limit=None):	
			try:
				self.links = self.links + ' ' + link.title
			except Exception as exc:
				print('{0} Saved comments make me throw this exception, I should check is this is absolutely necessary'.format(exc))
		return self.links
