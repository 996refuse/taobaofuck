#coding=utf8
#import os
#import sets
#import time
import Queue
import threading
#import collections

from search import TitleSearch
#from search import HtmlStore
from search import HtmlParser

import time, random

#输入文件每行以空白字符分割  取第一个作为关键字
#输入文件名gbk.txt输出out.txt
#默认utf8输入utf8输出
GBKIN = 0
GBKOUT = 0

SHARE_Q = Queue.Queue()
count = 0

class MyThread(threading.Thread):
	"""
	"""
	def __init__(self, func):
		super(MyThread, self).__init__()
		self.func = func
	
	def run(self):
		"""
		"""
		self.func()

def get_titles(filename):
	with open(filename, 'r') as f:
		for line in f:
			line = gbkIN(line)
			if '#' == line[0]:
				continue
			#title = line.rstrip('\r\n').split('\t')[1]
			title = line.rstrip('\r\n').split()[0]
			SHARE_Q.put(title)


def crawl_parse(title):
	
	global count
	global Error_count

	title_search = TitleSearch(title)
	url = title_search.gen_url()
	html = title_search.get_html(url)
	

	parser = HtmlParser(html)
	AnInt = parser.parse()

    
	if -1 == AnInt:
		SHARE_Q.put(title)
		print "### IndexError Retry", title
		time.sleep(random.random()*20 + 3)
		return

	if -2 == AnInt:
		SHARE_Q.put(title)
		print "### UnknowError Retry", title
		time.sleep(random.random()*100 + 3)
		return

	line = title.replace('\t', ' ')+'\t'+str(AnInt)+'\t'+'nz'+'\n'
	line = gbkOUT(line)
	with open('out.txt', 'a') as f:
		f.write(line)
    
	#print "### Accomplete", title
	count += 1

	if count%1000 == 0:
		print "### 已完成关键词个数: " , count
	
	# 60万框架 nz  gbk

def worker():
	"""
	"""
	global SHARE_Q
	while True:
		if not SHARE_Q.empty():
			title = SHARE_Q.get()
			crawl_parse(title)
			SHARE_Q.task_done()
		else:
			break

def main(filename):

	global SHARE_Q

	WORKER_THREAD_NUM = 12
	get_titles(filename)
	print '### generate queue finished'
	
	threads = []
	for i in xrange(WORKER_THREAD_NUM):
		thread = MyThread(worker)
		thread.start()
		threads.append(thread)
	
	for thread in threads:
		thread.join()
	
	SHARE_Q.join()
	print '### crawling finished'

def gbkIN(string):
	if GBKIN:
		return string.decode('utf8').encode('gbk')
	return string

def gbkOUT(string):
	if GBKOUT:
		return string.decode('utf8').encode('gbk')
	return string

if __name__ == "__main__":
	import sys
	main(sys.argv[1]) 
