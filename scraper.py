#!/usr/bin/env python
import urllib2
import csv
import pdb 
import time
import unicodedata
import random
import json
from lxml import etree
import urllib
import os
import random
import requests
import datetime
import math
import re 


def pickUA():
	user_agent_list = [
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
		"Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
		"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
		"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
		"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
		"Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
		"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
		"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
		"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
		"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
		"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
		"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
		"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
	   ]
	return random.choice(user_agent_list)

def unicode_to_string(types):
	try:
		types = unicodedata.normalize("NFKD", types).encode('ascii', 'ignore')
		return types
	except:
		return types

def makeRequest(url):
	tree = None
	try:
		time.sleep(random.randint(0,5))
		response = urllib2.urlopen(url, timeout=10).read()
		tree = etree.HTML(response)
	except:
		try:
			time.sleep(random.randint(0,5))
			req = urllib2.Request(url, None, {'User-agent' : pickUA() })
			response = urllib2.urlopen(req, timeout=10).read()
			tree = etree.HTML(response)
		except Exception as e:
			print e
			print "Error"
	return tree

def decode_address_to_coordinates(address):
	time.sleep(3)
	params = {
			'address' : address,
			'sensor' : 'false',
	}  
	url = 'http://maps.google.com/maps/api/geocode/json?' + urllib.urlencode(params)
	response = urllib2.urlopen(url)
	result = json.load(response)
	try:
			return result['results'][0]['geometry']['location']
	except:
			result = None

def write_data(data):
	with open('data.js', 'w') as outfile:
		outfile.write("var coordinates = ")
		json.dump(data, outfile)
		outfile.write(";")

def makeObj(addr):
	res = {}
	try:
		result = decode_address_to_coordinates(addr)
	except Exception as e:
		result = None
	if result != None:
		res['coordinates'] = [result['lng'], result['lat']]
		res['label'] = addr 
		print res
	return res 

def main():
	url = "http://www.menuism.com/restaurant-locations/chipotle-mexican-grill-164322/us"
	tree = makeRequest(url)
	i = 1
	locations = []
	for state in tree.xpath('//ul[@class="list-unstyled-links"]//@href'):
		stateTree = makeRequest(state)
		print "Scraping state # " + str(i) 
		for loc in stateTree.xpath('//ul[@class="list-unstyled-links"]//@href'):
			locs = makeRequest(loc)
			if locs != None:	
				try:
					addr = re.sub('\s+',' ', ' '.join(locs.xpath('//div[@class="map-info"]//text()'))).strip()
					print addr 
				except Exception as e:
					print e
				res = makeObj(addr)
				if res != {}:
					locations.append(res)
		i+=1
	write_data(locations)
main()