from rest_framework import serializers
from data_analysis.models import *

class CompanySerializer(serializers.ModelSerializer):
    installations = serializers.PrimaryKeyRelatedField(many=True, queryset=Gateway.objects.all())

    class Meta:
        model = Company
        fields = ('company_id', 'name', 'installations')
        read_only_fields = ('company_id',)

class InstallationSerializer(serializers.ModelSerializer):
    gateways = serializers.PrimaryKeyRelatedField(many=True, queryset=Gateway.objects.all())

    class Meta:
        model = Installation
        #fields = ('installation_id', 'name', 'gateways', )
        #fields = '__all__'
        exclude = ('storage_on_remote', 'remote_database_id')
        read_only_fields = ('installation_id',)


class GatewaySerializer(serializers.ModelSerializer):
    sensors = serializers.PrimaryKeyRelatedField(many=True, queryset=Sensor.objects.all())
    config = serializers.PrimaryKeyRelatedField(many=True, queryset=GatewayConfiguration.objects.all())
    #sensors = serializers.HyperlinkedRelatedField(many=True, view_name='sensor-detail', read_only=True)

    class Meta:
        model = Gateway
        fields = ('gateway_id', 'ip_address', 'sensors', 'installation', 'config')
        read_only_fields = ('gateway_id',)


class GatewayConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GatewayConfiguration
        fields = ('gateway', 'attribute', 'value')


class SensorSerializer(serializers.ModelSerializer):
    measurements = serializers.PrimaryKeyRelatedField(many=True, queryset=Measurement.objects.all())
    config = serializers.PrimaryKeyRelatedField(many=True,queryset=SensorConfiguration.objects.all())
    measurement_types = serializers.ListField()


    class Meta:
        model = Sensor
        fields = ('sensor_id', 'name', 'gateway_id', 'measurements', 'config', 'measurement_types')


class SensorConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorConfiguration
        fields = ('sensor', 'attribute', 'value')


class MeasurementSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(MeasurementSerializer, self).__init__(many=many, *args, **kwargs)

    class Meta:
        model = Measurement
        fields = ('measurement_id', 'sensor_id', 'timestamp', 'measurement_type', 'value')#''sensor_id''


class LiteMeasurementSerializer(serializers.ModelSerializer):
    #def __init__(self, *args, **kwargs):
    #    many = kwargs.pop('many', True)
    #    super(LiteMeasurementSerializer, self).__init__(many=many, *args, **kwargs)

    class Meta:
        model = Measurement
        fields = ('timestamp', 'value')

