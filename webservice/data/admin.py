from django.contrib import admin
from data.models import (Company, Gateway, Installation,
Measurement, MeasurementType, Sensor, )

class InstallationInline(admin.TabularInline):
    model = Installation
    extra = 1

class CompanyAdmin(admin.ModelAdmin):
    readonly_fields = ('company_id', )
    fieldsets = [
        (None,              {'fields': ['name']}),
        ('Info',            {'fields': ['company_id'], 'classes': ['collapse']}),
    ]
    inlines = [InstallationInline]
    list_display = ('name', 'company_id')
    search_fields = ['name']

class GatewayInline(admin.TabularInline):
    model = Gateway
    extra = 1

class InstallationAdmin(admin.ModelAdmin):
    readonly_fields = ('installation_id', )
    fieldsets = [
        (None,              {'fields': ['name']}),
        ('Info',            {'fields': ['installation_id'], 'classes': ['collapse']}),
    ]
    inlines = [GatewayInline]
    list_display = ('name', 'installation_id')
    search_fields = ['name']

class SensorInline(admin.TabularInline):
    model = Sensor
    extra = 1

class GatewayAdmin(admin.ModelAdmin):
    readonly_fields = ('gateway_id', )
    fieldsets = [
        (None,              {'fields': []}),
        ('Info',            {'fields': ['gateway_id'], 'classes': ['collapse']}),
    ]
    inlines = [SensorInline]
    search_fields = ['gateway_id']

class MeasurementInline(admin.TabularInline):
    model = Measurement
    extra = 0

class SensorAdmin(admin.ModelAdmin):
    readonly_fields = ('measurement_chart', 'sensor_id', )
    fieldsets = [
        (None,              {'fields': []}),
        ('Info',            {'fields': ['sensor_id'], 'classes': ['collapse']}),
        ('Measurements',      {'fields': ['measurement_chart',]}),
    ]
    inlines = [MeasurementInline]
    search_fields = ['sensor_id']

admin.site.register(Company, CompanyAdmin)
admin.site.register(Gateway, GatewayAdmin)
admin.site.register(Installation, InstallationAdmin)
admin.site.register(Measurement)
admin.site.register(MeasurementType)
admin.site.register(Sensor, SensorAdmin)
