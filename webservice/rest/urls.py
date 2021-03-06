from django.conf.urls import url, include
from rest import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

"""
Routing: 5 major routes.

Companies and Installations do not use nested routes.

The gateway entry point serves for both gateways, sensors and measurements.
It is the go to entry point for the physical node when pushing new data to the server.

A fourth and fifth entry point are for measurement types and alerts, they are independent of the hierarchy.

/companies/{}
/installations/{}

/gateways{} -> sensors -> measurements
                       -> measurement-types
                       -> config
            -> config

/measurement-types/
/alerts
"""

router = SimpleRouter()
router.register(r'companies', views.CompanyViewSet)
router.register(r'installations', views.InstallationViewSet)
router.register(r'gateways', views.GatewayViewSet)
router.register(r'measurement-types', views.MeasurementTypeViewSet)
router.register(r'user', views.UserViewSet)
router.register(r'alerts', views.AlertViewSet)

gateways_router = NestedSimpleRouter(router, r'gateways', lookup='gateway')
gateways_router.register(r'sensors', views.SensorViewSet)
gateways_router.register(r'config', views.GatewayConfigurationViewSet)

sensors_router = NestedSimpleRouter(gateways_router, r'sensors', lookup='sensor')
sensors_router.register(r'measurements', views.MeasurementViewSet)
sensors_router.register(r'config', views.SensorConfigurationViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(gateways_router.urls)),
    url(r'^', include(sensors_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
urlpatterns = format_suffix_patterns(urlpatterns)