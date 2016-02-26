from django.conf.urls import url, include
from rest import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers


router = routers.SimpleRouter()
router.register(r'companies', views.CompanyViewSet)
router.register(r'gateways', views.GatewayViewSet)

companies_router = routers.NestedSimpleRouter(router, r'companies', lookup='companies')
companies_router.register(r'installations', views.InstallationViewSet)

installations_router = routers.NestedSimpleRouter(companies_router, r'installations', lookup='installation')
installations_router.register(r'gateways', views.GatewayViewSet)

gateways_router = routers.NestedSimpleRouter(installations_router, r'gateways', lookup='gateway')
gateways_router.register(r'sensors', views.SensorViewSet)
gateways_router.register(r'config', views.GatewayConfigurationViewSet)

sensors_router = routers.NestedSimpleRouter(gateways_router, r'sensors', lookup='sensor')
sensors_router.register(r'measurements', views.MeasurementViewSet)
sensors_router.register(r'config', views.SensorConfigurationViewSet)


gateways_g_router = routers.NestedSimpleRouter(router, r'gateways', lookup='gateway')
gateways_g_router.register(r'sensors', views.SensorViewSet)

sensors_g_router = routers.NestedSimpleRouter(gateways_g_router, r'sensors', lookup='sensor')
sensors_g_router.register(r'measurements', views.MeasurementViewSet)


lite_router = routers.SimpleRouter()
lite_router.register(r'lite', views.LiteMeasurementView, 'lite')
#measurements_router = routers.NestedSimpleRouter(sensors_router, r'measurements', lookup='measurement')
#measurements_router.register(r'sensors', views.SensorViewSet)


# 'base_name' is optional. Needed only if the same viewset is registered more than once
# Official DRF docs on this option: http://www.django-rest-framework.org/api-guide/routers/

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(companies_router.urls)),
    url(r'^', include(installations_router.urls)),
    url(r'^', include(gateways_router.urls)),

    url(r'^', include(sensors_router.urls)),

    url(r'^', include(gateways_g_router.urls)),
    url(r'^', include(sensors_g_router.urls)),

    url(r'^lite', views.LiteMeasurementView.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^rest/sensors$', views.SensorList.as_view()),
    #url(r'^rest/sensors(?P<pk>[0-9]+)/$', views.SensorDetail.as_view()),
    #url(r'^rest/sensors/(?P<pk>[0-9]+)/$',
    #    views.SensorDetail.as_view(),
    #    name='sensor-detail'),
    
    
    #url(r'^rest/sensors/(?P<pk>[0-9]+)/highlight/$',
    #    views.SensorHighlight.as_view(),
    #    name='sensor-highlight'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
