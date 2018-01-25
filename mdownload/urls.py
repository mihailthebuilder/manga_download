#defines URL patterns for the main app
from django.conf.urls import include,url
from . import views

#NEEDS TO BE INCLUDED IN ORDER TO REMEMBER APP/VIEW NAMESPACE
app_name='mdownload'

urlpatterns = [
	#homepage
    url(r'^$', views.index,name='index'),
    
    #show all search results
	url(r'^search_results/$', views.search_results, name = 'search_results'),
    
    #show all chapters for single manga
    url(r'^manga_chapters/(?P<manga_id>\d+)/$', views.manga_chapters,name = 'manga_chapters'),
    
    #download chapter for a manga
    url(r'^chapter_download/(?P<chapter_id>\d+)/$', views.chapter_download, name='chapter_download'),
]


