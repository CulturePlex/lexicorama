# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('words.views',

    # index
    url(r'^$', 'search', name="search"),

)
