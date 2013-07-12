from django.conf.urls.defaults import *
from lab7.settings import ROOT

from learn import views

urlpatterns = patterns('',
    		url(r'^$', views.index, name='index'),
    		url(r'^index/$', views.index, name='index'),
    		url(r'^home/$', views.home, name='home'),
    		url(r'^edit/(?P<userId>\d+)/(?P<songId>\d+)/$', views.editSongDetails, name='edit'),
    		url(r'^view/(?P<userId>\d+)/(?P<songId>\d+)/$', views.viewSongDetails, name='view'),
		url(r'^move/(?P<userId>\d+)/(?P<songId>\d+)/(?P<fromlist>\d+)/(?P<tolist>\d+)/$', views.move, name='move'),
		url(r'^add/$', views.add, name='add'),
		url(r'^auth/login/$', views.login, name='login'),
		url(r'^auth/logout/$', views.logout, name='logout'),
		url(r'^auth/create/$', views.create, name='create'),
		url(r'^delete/(?P<userId>\d+)/(?P<songId>\d+)/$', views.delete, name='delete'),
		url(r'^api/login/(?P<_username>\w*)/(?P<_password>\w*)/$', views.api_login, name='api_login'),
		url(r'^api/logout/$', views.api_logout, name='api_logout'),
		url(r'^api/home/$', views.api_home, name='api_home'),
)


urlpatterns += patterns('',
                       (r'^static/(?P<path>.*)$',
                        'django.views.static.serve',
                        {'document_root': ROOT('learn/static/')}),
                       )
