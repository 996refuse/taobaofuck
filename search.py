#coding=utf8
#Base module provide TitleSearch class, HtmlStore class and HtmlParser class
import os
import re
import urllib
import requests
import socket


class TitleSearch(object):
	"""
	Title Search class
	"""
	def __init__(self, title):
		"""
		Init class using title.
		"""
		self.title = title
	
	def gen_url(self):
		"""
		generate url.
		"""
		encode_title = urllib.quote(self.title)
		taobao_url = 'http://s.taobao.com/search?q='+encode_title
		return taobao_url

	def get_html(self, url):
		"""
		get html content using taobao's url.
		"""
		try:
			page = requests.get(url)
			html = page.content
		except requests.exceptions.Timeout:
			html = self.title+'\t'+'requests timeout'
		except:
			html = self.title+'\t'+'Error'
		
		return html

'''
class HtmlStore(object):
	"""
	Store html.
	"""
	def __init__(self, directory, title):
		"""
		Init class using directory and title.
		"""
		self.directory = directory
		self.title = title

	
	def store(self, content):
		"""
		Store html to file.
		"""
		with open(os.path.join(self.directory, self.title), 'w') as f:
			f.write(content)
'''
	
class HtmlParser(object):
	"""
	Html Parser.
	"""

	def __init__(self, content):
		"""
		Init class using directory.
		"""
		self.content = content

	def parse(self):
		"""
		Parse html and return baobeiTotalHit.
		"""
		def __2int(string):
			if "万" in string:
				match = re.findall('(.*?)万', string)[0]
				return int(float(match) * 1e4)
			return int(string)

		regex = r'"baobeiTotalHit":"([^\"\']*?)"'
		targets = re.findall(regex, self.content)
		#print __2int(targets[0])
		try:
			return __2int(targets[0])
		except IndexError:
			print '### IndexError'
			#print self.content
			return -1
		except:
			print '### Error'
		        return -2

if __name__ == "__main__":
	pass
