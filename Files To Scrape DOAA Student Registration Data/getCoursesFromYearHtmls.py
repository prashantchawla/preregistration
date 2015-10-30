#######################################################################
"""
This code is used to parse the files Y20XX-YY.html and get the links to
grab the list of students enrolled in that particular course.
It then creates directories with name Y20XX-YY and fills this directory
with the files containing list of students enrolled in the course with
the file name being COURSENUMsem.html

"""
#######################################################################


import re
import mechanize
from bs4 import BeautifulSoup
from os import listdir
import os.path
import time

def find_between( s, first, last ):
	"""
	Finds the string in s that occurs between the substrings first and last
	and returns it 
	"""
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return (s[start:end]).strip()


def getFilesInDir(directory):
	"""
	Creates a list of files (not directories) in the "directory" folder.
	"directory" must be a string of the form "/home/deepak/......../FolderContainingY20XX-YY.htmlFiles"
	"""
	return [ f for f in listdir(directory) if os.path.isfile(os.path.join(directory,f)) ]

def getLinks(htmltext):
	"""
	Parses the htmltext and grabs all the links in <a> tag. Attaches this relative
	link to the string "http://172.26.142.68/dccourse/" to generate the downloadable
	link. Also finds the course, sem, acadyr corresponding to this particular link.
	Returns a list like:
	[["2012-13", "2", "TA201A", "http://............"], ["2012-13", "1", "CS350A", "http://......"]]
	"""
	soup = BeautifulSoup(htmltext, "lxml")
	listOfATagsWhole = soup.find_all("a")
	listOfATags = []
	for wholetag in listOfATagsWhole:
		listOfATags.append(str(wholetag["href"]))
	listOfListOfLinks = []
	for i in range(len(listOfATags)):
		courselink = "http://172.26.142.68/dccourse/" + str(listOfATags[i])
		coursename = find_between(str(listOfATags[i]), "course_no=", "&")
		acadyr = find_between(str(listOfATags[i]), "acad_year=", "&")
		sem = str(listOfATags[i])[-1]
		listOfListOfLinks.append(list((acadyr, sem, coursename, courselink)))
	return listOfListOfLinks


start_time = time.time()
old_time = time.time()

filesInDir = getFilesInDir("./")
for i in range(len(filesInDir)):
	if (str(filesInDir[i]).endswith(".html")):  # If html file
		newdirname = "./" + '.'.join(filesInDir[i].split(".")[:-1]) # Create name like "./Y2011-12"
		if not os.path.exists(newdirname): # If directory doesn't exist
			os.makedirs(newdirname)
			yrfile = open(str(filesInDir[i]), 'r')   # Open file "Y2011-12.html" to read and parse
			listOfListOfLinks = getLinks(yrfile.read())  # Parse the html and generate the course links and info
			for courselist in listOfListOfLinks:
				filename = str(courselist[2]) + str(courselist[1]) + ".html"; 
				fd = open(newdirname+"/"+filename, 'w')
				# There is some problem with the function htmlmerge. It changed
				# the "&" in the link to "&amp;". Hence we change it back to "&"
				newurl = str(courselist[3]).replace("&amp;", "&")
				# print newurl
				page = mechanize.urlopen(newurl)
				fd.write(page.read())
				fd.close()

	TimeTaken = time.time() - old_time
	old_time = time.time()
	print "Done" + newdirname
	print("Time Taken to get OneYear's Data: %s seconds \n" %(TimeTaken))


TotalTimeTaken = time.time() - start_time
print("Total Time Taken: %s \n" %(TotalTimeTaken))
