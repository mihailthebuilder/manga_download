#--STANDARD LIBARIES--
#render sends to page with context
from django.shortcuts import render

#httpresponseredirect redirects user to the same page once request posted
#http404 obviously raises dat error
from django.http import HttpResponseRedirect, Http404, HttpResponse

#reverse determines url from named url pattern so you don't have to
#write whole url all over again
from django.urls import reverse

#messages stores info from one view to move to another view
from django.contrib import messages
from django.contrib.messages import get_messages

#enables you to create temporary directories that get deleted after usage
from tempfile import TemporaryDirectory

#allows you to work with directory paths
import os

#import a django method that enablesy you to return a text object
from django.utils.encoding import smart_str

#--CUSTOM CODE--
#import form and custom functions
from .forms import SearchForm
from .custom_functions import mangaSearch, getChapters, pdfCreatePath

# Create your views here.
def index(request):
	"""homepage"""	
	#check if we've posted a search request
	if request.method != 'POST':
		#no data submitted, create a blank form
		form = SearchForm()
	else:
		#search request submitted, first get a copy of the form
		form = SearchForm(request.POST)
		
		if form.is_valid():
			
			#get the search input from the submitted form
			searchInput = form.clean().get("search_input")
			
			#use the input in the form to search for results
			mangas = mangaSearch(searchInput)
			
			#save the search input and results for rendering in the next view
			request.session['searchResults'] = mangas
			request.session['searchInput'] = searchInput
						
			#go to results with the results already saved in 'messages'
			return HttpResponseRedirect(reverse('mdownload:search_results'))

	context = {'form':form}
	return render(request,'mdownload/index.html',context)

def search_results(request):
	"""manga search results page"""	
	#get the search input and results results from the session into a context
	context = {'searchResults': request.session['searchResults'],'searchInput':request.session['searchInput']}
	#then render the page with the results stored into context
	return render(request,'mdownload/search_results.html',context)

def manga_chapters(request, manga_id):
	"""list of chapters for given manga"""
	#get manga title (0) and url (1)
	manga_pair = request.session['searchResults'][int(manga_id)]
	#get list of chapters and links from url of manga
	chapters = getChapters(manga_pair[1])
	
	#save chapters variable in session cookie so you can access in another view
	request.session['chaptersList'] = chapters
	
	#also send chapters variable in page that lists all chapters
	context = {'chaptersList': chapters,'mangaTitle':manga_pair[0]}
	return render(request,'mdownload/manga_chapters.html',context)

def chapter_download(request, chapter_id):
	"""downloads a PDF copy of the chapter into your browser"""
	#get front link of chapter from session
	chapter_link = request.session['chaptersList'][int(chapter_id)][1]

	#create temporary directory
	with TemporaryDirectory() as td:
				
		#build PDF copy of file on server and get its path
		manga_path = pdfCreatePath(chapter_link,td)
				
		#open file for delivery
		content_file = open(manga_path, 'rb')
		#include file in response object
		response = HttpResponse(content=content_file)
		#add headers which indicate it's a pdf file with chapter.pdf name...
		#...which should be delivered as a downloaded file
		response['Content-Type']='application/pdf'
		response['Content-Disposition'] = "attachment; filename=chapter.pdf"
		
		#set cookie so that loading image gets hidden by main.js
		response.set_cookie('downloadFinished', 'true')
		
		#return the response object with the file
		return response
