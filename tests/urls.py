# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from .example.views import TestView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('chat/', include('tests.example.urls')),
    path('test/', TestView.as_view()),
]
