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
	def __init__(self, title, title_count):
		"""
		Init class using title.
		"""
		self.title = title
		self.title_count = title_count
	
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
		
		print self.title_count, len(html)
		return html

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
	

class HtmlParser(object):
	"""
	Html Parser.
	"""

	def __init__(self, content):
		"""
		Init class using directory.
		"""
		self.content = content
	

	def parse(self, filename):
		"""
		Parse html and return keyword.
		"""
		general_regex = r'我们为您找到了.*?的搜索结果|搜索结果较少，尝试下.*?"export":false}'
		target_strs = re.findall(general_regex, self.content)
		regex = r'\u003e.*?\u003c'
		keywords = []
		try:
			words = re.findall(regex, target_strs[0])
			for word in words:
				keyword = word.lstrip('\u003e').rstrip('\u003c')
				keywords.append(keyword)
		except IndexError:
			return filename
		except:
		        return 'ERROR'

		return ' '.join(keywords)
	

if __name__ == "__main__":
	pass
