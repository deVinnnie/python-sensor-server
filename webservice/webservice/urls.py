from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = patterns('',
    url(r'^data/', include('data.urls', namespace="data")),
    url(r'^configuration/', include('configuration.urls', namespace="configuration")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rest/', include('rest.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', RedirectView.as_view(url='/api-auth/login/?next=/rest/companies/')), # 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
)
