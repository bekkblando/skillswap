"""skillswap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from swap.views import home, SkillLookup, add_skill, register, profile, KnowDeleteView, LearnDeleteView, UserPageView, userchatview, \
    ChatListView, meetingcreate
from django.contrib.auth.views import login, logout


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'addskill/$', add_skill, name="addskill"),
    url(r'^register/$', register, name="register"),
    url(r'^skill_lookup/$', SkillLookup.as_view(), name="skilllookup"),
    url(r'^accounts/login/', login, name="login"),
    url(r'^logout/', logout, {'next_page': '/'}, name="logout"),
    url(r'^profile/$', profile, name="profile"),
    url(r'userpage/(?P<pk>\d+)', UserPageView.as_view(), name='userpage'),
    url(r'deleteknow(?P<pk>\d+)',KnowDeleteView.as_view(), name="deleteknow" ),
    url(r'deletelearn(?P<pk>\d+)',LearnDeleteView.as_view(), name="deletelearn" ),
    url(r'createuserchat', userchatview, name="userchatcreate"),
    url(r'createmeeting', meetingcreate, name="meetingcreate"),
    url(r'chat/', ChatListView.as_view(), name='chatlist'),
    url(r'', home, name="home"),
]
