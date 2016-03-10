from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^data/', include('data.urls', namespace="data")),
    url(r'^configuration/', include('configuration.urls', namespace="configuration")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rest/', include('rest.urls'))
)
