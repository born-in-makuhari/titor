from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^titor/', include('titorApp.urls')),
)

if not settings.DEBUG:
      urlpatterns += patterns(
          '',
          (
              r'^static/(?P<path>.*)$',
              'django.views.static.serve',
              {'document_root': settings.STATIC_ROOT}
          ),
      )
