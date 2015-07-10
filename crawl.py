#coding=utf8
import os
import sets
import time
import Queue
import threading
import collections

from search import TitleSearch
from search import HtmlStore
from search import HtmlParser


SHARE_Q = Queue.Queue()
Error_count = 0
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
			#title = line.rstrip('\r\n').split('\t')[1]
			title = line.rstrip('\r\n')
			SHARE_Q.put(title)


def crawl_parse(title):
	
	global count
	global Error_count

	new_title = '南京'+title
	title_search = TitleSearch(new_title, count)
	taobao_url = title_search.gen_url()
	html = title_search.get_html(taobao_url)
	
	html_parser = HtmlParser(html)
	strs = html_parser.parse(title)
        
	#html_store = HtmlStore(directory, str(count))
        
	try:
		with open('Index_newword', 'a') as f:
            		f.write(title+'\t'+strs+'\n')
	except:
		Error_count += 1
	
	count += 1
	if count%10000 == 0:
		print count
	
	#try:
	#	html_store.store(title+'\t'+strs)
	#except:
	#	Error_count += 1
	#	pass


def worker():
	"""
	"""
	global SHARE_Q
	while True:
		if not SHARE_Q.empty():
			title = SHARE_Q.get()
			crawl_parse(title)
			SHARE_Q.task_done()

def main(filename):

	global SHARE_Q

	WORKER_THREAD_NUM = 20
	get_titles(filename)
	print 'generate queue finished'
	
	threads = []
	for i in xrange(WORKER_THREAD_NUM):
		thread = MyThread(worker)
		thread.start()
		threads.append(thread)
	
	for thread in threads:
		thread.join()
	
	SHARE_Q.join()
	print 'crawling finished'

if __name__ == "__main__":
	main('Index_error')
