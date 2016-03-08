from django.conf.urls import patterns, url

from django.conf import settings

from data import views

urlpatterns = patterns('',
    url (
        regex = r'^$',
        view = views.IndexView.as_view(),
        name = 'index'
    ),
    
    url (
        regex = r'^companies$',
        view = views.companyView,
        name = 'companies'
    ),

    url (
        regex = r'^companies/(?P<pk>\d+)/installations$',
        view = views.CompanyDetailView.as_view(),
        name = 'company_detail'
    ),
    
    url (
        regex = r'^companies/(?P<company_pk>\d+)/installations/(?P<pk>\d+)/gateways$',
        view = views.InstallationDetailView.as_view(),
        name = 'installation_detail'
    ),
    
     url (
        regex = r'^companies/(?P<company_pk>\d+)/installations/(?P<installation_pk>\d+)/gateways/(?P<pk>\d+)/sensors$',
        view = views.GatewayDetailView.as_view(),
        name = 'gateway_detail'
    ),
    
    url (
        regex = r'^companies/(?P<company_pk>\d+)/installations/(?P<installation_pk>\d+)/gateways/(?P<gateway_pk>\d+)/sensors/(?P<pk>\d+)/measurements$',
        view = views.SensorDetailView.as_view(),
        name = 'sensor_detail'
    )
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
