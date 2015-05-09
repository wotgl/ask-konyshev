__author__ = 'sasha1003'

from django.contrib import admin
from django.conf.urls import patterns, include, url

from core.views import main, question, tag, signup, login_view, logout_view, base, ask, new_answer
from core.views import settings, edit_profile, change_password, edit_photo, profile, like,  create_post

#TODO:	add regular to username -> 1 word

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	url(r'^$', main, name='index'),
	url(r'^popular/', main, name='popular'),
	url(r'^question/(?P<question_id>\d+)/$', question, name='question'),
	url(r'^new_answer/', new_answer, name='new_answer'),
	url(r'^tag/(?P<tag_name>\w+)/$', tag, name='tag'),
	url(r'^signup/', signup, name='signup'),
	url(r'^login/', login_view, name='login'),
	url(r'^logout/', logout_view, name='logout'),
	url(r'^base/', base, name='base'),
	url(r'^ask/', ask, name='ask'),
	url(r'^settings/', settings, name='settings'),
	url(r'^edit_profile/', edit_profile, name='edit_profile'),
	url(r'^change_password/', change_password, name='change_password'),
	url(r'^edit_photo/', edit_photo, name='edit_photo'),
	url(r'^profile/(?P<username>\w+)/$', profile, name='profile'),

	url(r'^like/', like, name='like'),
	url(r'^create_post/', create_post, name='create_post'),
)



