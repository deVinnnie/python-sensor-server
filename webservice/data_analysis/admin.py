from django.contrib import admin
from data_analysis.models import (Company, Gateway, GatewayConfiguration, Installation,
Measurement, MeasurementType, Sensor,)

class InstallationInline(admin.TabularInline):
    model = Installation
    extra = 1

class CompanyAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['name']}),
        ('Info',            {'fields': ['company_id'], 'classes': ['collapse']}),
    ]
    inlines = [InstallationInline]
    list_display = ('name', 'company_id')
    
admin.site.register(Company, CompanyAdmin)
admin.site.register(Gateway)
admin.site.register(GatewayConfiguration)
admin.site.register(Installation)
admin.site.register(Measurement)
admin.site.register(MeasurementType)
admin.site.register(Sensor)
