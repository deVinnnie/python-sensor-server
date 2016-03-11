from rest_framework import serializers
from data.models import *
from configuration.models import *

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


class SensorSerializer(serializers.ModelSerializer):
    config = serializers.PrimaryKeyRelatedField(many=True,queryset=SensorConfiguration.objects.all())
    #measurement_types = serializers.ListField(read_only=True)

    class Meta:
        model = Sensor
        fields = ('sensor_id', 'name', 'gateway',
                  #'measurement_types',
                  'config')
        read_only_fields = ('sensor_id')


class GatewaySerializer(serializers.ModelSerializer):
    sensors = SensorSerializer(many=True, read_only=True)
    #sensors = serializers.PrimaryKeyRelatedField(many=True, queryset=Sensor.objects.all())
    config = serializers.PrimaryKeyRelatedField(many=True, queryset=GatewayConfiguration.objects.all())

    class Meta:
        model = Gateway
        fields = ('gateway_id', 'ip_address', 'sensors', 'installation', 'config')
        read_only_fields = ('gateway_id',)


class GatewayConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GatewayConfiguration
        fields = ('attribute', 'value')





class SensorConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorConfiguration
        fields = ('attribute', 'value')


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


class MeasurementTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeasurementType
        fields = ('measurementTypeID', 'name', 'unit', 'scalar')
