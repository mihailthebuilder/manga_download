#this is where I store all custom functions for the manga download

#requests opens websites, bs4 (BeautifulSoup) parses thru html
#NEED MORE COMMENTS...
import requests, bs4, os, re, PyPDF2, shutil
from PIL import Image


def pullSoup(front_url, selector):
	"""pulls soup list from front part of mangapanda url and selector """
	#add base url to front url to get complete url for page to be opened
	full_url = "http://www.mangapanda.com" + front_url
	#open up page
	resPage = requests.get(full_url)
	#check for errors
	resPage.raise_for_status()
	#return list of results using beautifulsoup
	return(bs4.BeautifulSoup(resPage.text,"lxml").select(selector))

def mangaSearch(searchInput):
	"""takes search input and returns list of manga results from mangapanda.com"""
	#gets the list of soup elements from url (first input) using the selector (second input)	
	soupList = pullSoup("/search/?w="+searchInput,'.mangaresultitem a')
	#reshape so that it is a list of front link+title elements
	#this is identical to below but will change in the future once core fully functional
	resultList = []
	for result in soupList:
		element = [result.getText(), result.get("href")]
		resultList.append(element)
		
	return(resultList)
	# get the core functionality out first, then build upon it.
	#next get images, tags and other stuff

def getChapters(manga_url):
	"""takes manga url and returns list of chapters together with their link"""
	#gets the list of soup elements from url (first input) using the selector (second input)
	soupList = pullSoup(manga_url,'#listing a')
	#reshape so that it is a list of front link+title elements
	#this won't change even after making changes above
	resultList = []
	for result in soupList:
		element = [result.getText(), result.get("href")]
		resultList.append(element)
	
	#reverse the list in descending order of chapters
	resultList.reverse()
	return(resultList)
	

def makePdf(inputPath, outputFileName):    
    """makePdf makes PDF from all images in folder and deletes the folder"""
    #Add all pdf pages in chapter folder to a single pdf object
    pdfOutputObject = PyPDF2.PdfFileWriter()    
    for filename in os.listdir(inputPath):
        pdfPage = PyPDF2.PdfFileReader(inputPath+"\\"+filename)
        pageObj = pdfPage.getPage(0)
        pdfOutputObject.addPage(pageObj)
    
    #download pdf object to main folder
    pdfOutputFile = open(os.path.join(inputPath,outputFileName),"wb")
    pdfOutputObject.write(pdfOutputFile)

def storeChapterImgs(chapter_url, directory):
	"""downloads all chapter pages as individual PDF images into the directory """
	#get chapter index which will be used to check whether we went to another chapter
	#not sure why you need to use findall as opposed to match but it works, match doesn't
	url_regex = re.compile(r"/\d+")
	chapter_index = url_regex.findall(chapter_url)[0]
	
	#while you are still at the same chapter...
	while chapter_url.find(chapter_index) != -1:
		#in soup look for img tag in manga chapter page
		imgData = pullSoup(chapter_url,"#img")

		#get link to image file and name of the image
		imgLink = imgData[0].get("src")
		imgTitle = imgData[0].get("alt")
		
		#access the image file from link
		resImg = requests.get(imgLink)

		#change imageTitle so that it shows Attack on Titan - Page 05 instead of [...]Page 5
		#!!!this is essential to keep pages in the right order!!!
		titleRegex = re.compile(r" (?=\d$)")
		imgPath = os.path.join(directory,titleRegex.sub(" 0",imgTitle))+".jpg"
		
		#Download image to chapter pages folder in jpg format
		imgFile = open(imgPath,'wb')
		for chunk in resImg.iter_content(100000):
			imgFile.write(chunk)
		imgFile.close()
		
		#Convert image to pdf format and delete jpg
		im = Image.open(imgPath)
		#take out last 4 characters (".jpg")
		im.save(imgPath[:-4]+".pdf",resolution = 100.0)
		os.unlink(imgPath)
			
		#Return next button
		chapter_url = pullSoup(chapter_url,".next a")[0].get("href")   
	
	
def pdfCreatePath(chapter_url, directory):
	"""takes chapter url and stores a PDF copy of the chapter on server"""

	#download all pages as images into the directory
	storeChapterImgs(chapter_url, directory)
	
	#convert all image pages into a single PDF
	makePdf(directory,"chapter.pdf")
			
	#return path of PDF file
	return os.path.join(directory,"chapter.pdf")
