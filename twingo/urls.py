# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns('twingo_oauth',
    url(r'^login/$', 'twingo.views.twitter_login', name='twingo_login'),
    url(r'^callback/$', 'twingo.views.twitter_callback', name='twingo_callback'),
    url(r'^logout/$', 'twingo.views.twitter_logout', name='twingo_logout'),
)
