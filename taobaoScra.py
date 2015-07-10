#!/usr/bin/env python

import requests
import re
import json

def getCatalogs():
	response = requests.get(u"http://s.taobao.com/list?spm=a21bo.7724922.8407-line-7.9.XBH2ji&style=grid&seller_type=taobao&cps=yes&auction_tag%5B%5D=12034&scm=1007.12013.7925.100000000000000&cat=")
	response.encoding = "UTf8"
	cats = re.findall('"text":"([^"]*?)"[^{}]*"value":"(\d*?)","trace":"navPropertyNew"', response.text)
	return cats

class urlASM(dict):
    def __init__(self, catsID):
        self.catsID = catsID
    def __missing__(self, key):
        if 1 == key:
            return "http://s.taobao.com/list?data-key=s&data-value=0&ajax=true&callback=jsonp3009&style=grid&seller_type=taobao&cps=yes&auction_tag%5B%5D=12034&cat="+self.catsID+"&bcoffset=0&s=60"
        return "http://s.taobao.com/list?data-key=s&data-value="+str((key-1)*60)+"&ajax=true&callback=jsonp3339&style=grid&seller_type=taobao&cps=yes&auction_tag%5B%5D=12034&cat="+self.catsID+"&bcoffset=0&s="+str((key-1)*60)

def json2info(jsonObj):
	for i in jsonObj["mods"]["itemlist"]["data"]["auctions"]:
	    yield i["raw_title"], i["detail_url"], i["view_price"]

def timeOut():
	## Time Out 3~6 s
	import time, random
	t = random.random()*3+3
	time.sleep(t)
	print "### Sleep: ", t

def main():
	for clName, clNum in getCatalogs():
		urlFac = urlASM(clNum)
		for page in range(1,4):
			timeOut()
			response = requests.get(urlFac[page])
			response.encoding = "UTf8"
			try:
				decoded = json.loads(response.text[12:-2])
			except:
				print "### Error: url", clNum , page , urlFac[page]
				continue

			'''
			try:
				with open('tb.log','w') as fileObj:
					for title, url, price in json2info(decoded):
						fileObj.write(u'\t'.join([clName, clNum, title, url, price]) + '\n')
					fileObj.flush()
					print "### Accomplish: ", clNum , page 
			except:
				print "### Error: json", clNum , page
				continue
			'''
			with open('tb.log','w') as fileObj:
				for title, url, price in json2info(decoded):
					string = '\t'.join([clName.replace('\t', ' ').encode('UTF8'), clNum.replace('\t', ' ').encode('UTF8'), title.replace('\t', ' ').encode('UTF8'), url.replace('\t', ' ').encode('UTF8'), price.replace('\t', ' ').encode('UTF8')]) + '\n'
					fileObj.write(string)
				fileObj.flush()
				print "### Accomplish: ", clNum , page 
					
if __name__ == '__main__':
	main()