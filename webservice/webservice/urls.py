from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    url(r'^data/', include('data.urls', namespace="data")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rest/', include('rest.urls')),
    #url(r'^$', auth_views.login),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', RedirectView.as_view(url='/api-auth/login/?next=/rest/companies/')),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
)
