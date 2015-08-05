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
from swap.views import home, SkillLookup, add_skill, register, profile, knowdelete, learndelete, UserPageView, userchatview, \
    ChatListView, meetingcreate, MessagesListView, MessagesCreateView, UpdateProfile, SkillZipcode, geo_skills, addlearn
from django.contrib.auth.views import login, logout


urlpatterns = [

    url(r'^search/', include('haystack.urls')),
    url(r'zipcodesearch/(?P<zip>\d+)',SkillZipcode.as_view(), name='zipcode' ),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/update/$', UpdateProfile.as_view(), name='update_user'),
    url(r'addskill/$', add_skill, name="addskill"),
    url(r'^register/$', register, name="register"),
    url(r'^skill_lookup/$', SkillLookup.as_view(), name="skilllookup"),
    url(r'^accounts/login/', login, name="login"),
    url(r'^accounts/profile/', profile),
    url(r'^logout/', logout, {'next_page': '/home'}, name="logout"),
    url(r'^profile/$', profile, name="profile"),
    url(r'userpage/(?P<pk>\d+)', UserPageView.as_view(), name='userpage'),
    url(r'deleteknow/(?P<pk>\d+)',knowdelete, name="deleteknow" ),
    url(r'deletelearn/(?P<pk>\d+)',learndelete, name="deletelearn" ),
    url(r'createuserchat', userchatview, name="userchatcreate"),
    url(r'createmeeting', meetingcreate, name="meetingcreate"),
    url(r'geo_skills', geo_skills, name="geo_skills"),
    url(r'addlearn', addlearn, name="addlearn"),
    url(r'chat/', ChatListView.as_view(), name='chatlist'),
    url(r'messagelist(?P<pk>\d+)', MessagesListView.as_view(), name='messagelist'),
    url(r'sendmessage/', MessagesCreateView.as_view(), name='messagecreate'),
    url(r'home', home, name="home"),
    url(r'^', home, name="hom"),

]
