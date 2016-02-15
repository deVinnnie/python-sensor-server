from django.conf.urls import patterns, url

from data_analysis import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^companies$', views.companyView, name='companies'),
    url(r'^company-(?P<pk>\d+)/instalations$', views.CompanyDetailView.as_view(), name='company_detail'),
    url(r'^installation-(?P<pk>\d+)/gateways$', views.InstallationDetailView.as_view(), name='installation_detail'),
    url(r'^gateway-(?P<pk>\d+)/sensors$', views.GatewayDetailView.as_view(), name='gateway_detail'),
    url(r'^sensor-(?P<pk>\d+)/measurements$', views.SensorDetailView.as_view(), name='sensor_detail'),
)
