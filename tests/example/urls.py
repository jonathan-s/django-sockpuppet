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

from .views import example

urlpatterns = [
    path('test/', example.ExampleView.as_view(), name='example'),
    path('param/', example.ParamView.as_view(), name='param'),
    path('test-static/', example.StaticView.as_view(), name='static'),
    path('progress/', example.ProgressView.as_view(), name='progress'),
    path('error/', example.ErrorView.as_view(), name='error'),
    path('users/', example.UserList.as_view(), name='user'),
]
