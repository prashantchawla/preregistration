import urllib2
from bs4 import BeautifulSoup
import time
import requests
from requests.auth import HTTPProxyAuth

proxy = {'http': 'http://ironport1.iitk.ac.in:3128'}
auth = HTTPProxyAuth('chawlap', 'password')

oarsurl = "http://oars.cc.iitk.ac.in:4040/Utils/CourseInfoPopup.asp?Course="
with open("scrape.txt") as f:
    courses = f.readlines()
    
for i in range(len(courses)):
	try:
		print oarsurl+courses[i].rstrip()
		#~ response = urllib2.urlopen(oarsurl+courses[i].rstrip())
		r = requests.get(oarsurl+courses[i].rstrip(), proxies=proxy, auth=auth)
		soup = BeautifulSoup(r.text, "html.parser")
		table = soup.find('table')
		if(str(table)=="None"):
			print courses[i]
			time.sleep(5)
		else:
			time.sleep(5)
		
		text_file = open("info/"+courses[i].rstrip()+".txt", "w")
		text_file.write(str(table))
		text_file.close()
	except:
		print courses[i]
