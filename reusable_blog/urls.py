from django.conf.urls import url
import views
 
urlpatterns = [
    url(r'^$', views.post_list),
    url(r'^top5$', views.post_list_top5),
	url(r'^(?P<id>\d+)/$', views.post_detail),    
	url(r'^post/$', views.new_post, name='new_post'),
	url(r'^(?P<id>\d+)/edit$', views.edit_post, name='edit'),	
]

