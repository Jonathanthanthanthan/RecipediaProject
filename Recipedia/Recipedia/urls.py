"""Recipedia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
'''This method takes the inputs from the LoginForm text fields and checks if password is associated with the username.

           Args:
                username (String) : The username that will be used to retrieve an assocated password hash.

                password (String) : The password that will be turned into a hash and be compared with the usernames associated password hash.

           Returns:
                   True if the password that was passed matches the password assosicated with the username that was passed.

                   False if the password that was passed does not match the password associated wiht the username that was passed.


'''
urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
