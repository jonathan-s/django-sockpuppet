"""example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.urls import path

from .views.example import ExampleView, ParamView, ProgressView, StaticView

urlpatterns = [
    path('test/', ExampleView.as_view(), name='example'),
    path('param/', ParamView.as_view(), name='param'),
    path('test-static/', StaticView.as_view(), name='static'),
    path('progress/', ProgressView.as_view(), name='progress')
]
