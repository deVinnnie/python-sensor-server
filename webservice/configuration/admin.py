from django.contrib import admin
from configuration.models import (SensorConfiguration, GatewayConfiguration, )

admin.site.register(GatewayConfiguration)
admin.site.register(SensorConfiguration)