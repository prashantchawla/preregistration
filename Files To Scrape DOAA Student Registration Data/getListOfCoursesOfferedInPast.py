##############################################################
"""
This is the first script to run. It finds out the list of courses
offered in each of the past years. Stores this list as .html file
After running this script. Run getcoursesfromyearhtmls.py
(make sure
you dont hava any other html files apart from those generated
by running this current script)

"""
##############################################################


import re
import mechanize
from bs4 import BeautifulSoup



def htmlMerge(htmlText1, htmlText2):
	"""
	Takes two html snippets (containing tables) and finds the rows in htmlText2 and appends it after the rows
	of htmlText1
	"""
	soup1 = BeautifulSoup(htmlText1, "lxml")
	table1 = soup1.find("table")
	soup2 = BeautifulSoup(htmlText2, "lxml")
	table2 = soup2.find("table")
	text2 =  '\n'.join(map(str, table2.contents[1:]))
	soup1.table.append(text2)
	#print soup1
	#print str(soup1.contents)

	newstr = ""
	for tag in soup1.contents:
		newstr = newstr + str(tag)
	newstr = newstr.replace("&lt;", "<")
	newstr = newstr.replace("&gt;", ">")
	return newstr


def getAcadYrList(myform):
	"""
	Takes a form object as returned by the funtion br.forms()[0] of mechanize package and
	returns the list of items under the acadyr dropdown
	"""
	tempList = []
	for i in range(len(myform.controls[11].get_items())-1):	#11 is for AcadYrOption
		tempList.append(myform.controls[11].get_items()[i+1]) #0th entry is * which means all(we don't want this)
	tempstr = '\t'.join(map(str,tempList))
	acadYrList = tempstr.split('\t')
	return acadYrList

#Using this list because the site takes longer than 60sec for each academic year. But a query can run only for 60sec. Hence we do it word by word for course number
alphabetList = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]


br = mechanize.Browser()
br.open("http://172.26.142.68/dccourse/")
br.select_form(name = "form1")
forms = [f for f in br.forms()] #Create list of all form objects in the page
myform = forms[0]  #form 0 is the only form in this page
acadYrList = getAcadYrList(myform)
#print acadYrList

#Create list of [List of AcadYrs]
acadYrListOfList = []
for i in range(len(acadYrList)):
	singletonlist = []	
	singletonlist.append(acadYrList[i])
	acadYrListOfList.append(singletonlist)

#Loop over the AcadYrListing
for yearList in acadYrListOfList:
	finalhtml = ""
	firstTime = True
	for i in range(len(alphabetList)):
		br.select_form(name = "form1")
		br["acadyr"] = yearList  # yearList must be a list. Refer to mechanize doc for more info
		br["coursename"] = alphabetList[i]
		response = br.submit()
		if firstTime:
			finalhtml = str(response.read())
			firstTime = False
		else:
			finalhtml = htmlMerge(finalhtml, str(response.read()))
		br.back()
		br.reload()
	filename = "Y" + yearList[0] + ".html"
	with open(filename, 'w') as fid:
		fid.write(finalhtml)
	print filename

print "Done"
