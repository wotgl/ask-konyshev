__author__ = 'sasha1003'

from django.conf.urls import patterns, include, url
from core.views import index, signup, login, base, question, ask
urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^signup/', signup),
    url(r'^login/', login),
    url(r'^base/', base),
    url(r'^question/', question),
    url(r'^ask/', ask),
)
