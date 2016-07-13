from django.conf.urls import patterns, include, url
from django.contrib import admin
from titorApp.views import AboutView
from titorApp.views import MonthData
from . import views

urlpatterns = patterns('titorApp.views',
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^titor/$', AboutView.as_view()),
    url(r'^month/$', MonthData.as_view()),
)
