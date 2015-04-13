__author__ = 'sasha1003'

from django.contrib import admin
from django.conf.urls import patterns, include, url

from core.views import index, popular, tag, signup, login, base, question, ask

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	url(r'^$', index, name='index'),
	url(r'^popular/', popular, name='popular'),
	#r'^(?P<question_id>\d+)/$'
	url(r'^tag/(?P<tag_name>\w+)/$', tag, name='tag'),
	url(r'^signup/', signup, name='signup'),
	url(r'^login/', login, name='login'),
	url(r'^base/', base, name='base'),
	url(r'^question/', question, name='question'),
	url(r'^ask/', ask, name='ask'),
)

