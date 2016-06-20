from django.conf.urls import patterns, include, url
from django.contrib import admin
from titorApp.views import AboutView
from . import views

urlpatterns = patterns('titorApp.views',
    # Examples:
    # url(r'^$', 'titor.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^titor/$', AboutView.as_view()),
    url(r'^titor/json/$', views.line_chart_json,
        name='line_chart_json'),
)
