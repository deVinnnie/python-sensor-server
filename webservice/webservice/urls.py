from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^data_analysis/', include('data_analysis.urls', namespace="data_analysis")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rest/', include('rest.urls'))
)
