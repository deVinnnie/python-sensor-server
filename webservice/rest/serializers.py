from rest_framework import serializers
from data.models import *

class AlertSerializer(serializers.ModelSerializer):

    class Meta:
        model = Alert
        fields = ('id', 'text', 'url', 'company', 'archived', 'gateway', 'sensor', 'measurementTypeID', 'type_name')
        read_only_fields = ('id', 'company', 'gateway', 'sensor', 'measurementTypeID')


class SensorConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorConfiguration
        fields = ('sensor', 'gateway', 'id', 'attribute', 'value', 'confirmed')


class SensorSerializer(serializers.ModelSerializer):
    config = SensorConfigurationSerializer(many=True, read_only=True)
    #serializers.PrimaryKeyRelatedField(many=True,queryset=SensorConfiguration.objects.all())
    #measurement_types = serializers.ListField(read_only=True)

    alerts = AlertSerializer(many=True, read_only=True)

    class Meta:
        model = Sensor
        fields = ('sensor_id', 'name', 'gateway',
                  #'measurement_types',
                  'config', 'position_long', 'position_lat', 'alerts')
        read_only_fields = ('sensor_id')


class GatewayConfigurationSerializer(serializers.ModelSerializer):

    class Meta:
        model = GatewayConfiguration
        fields = ('id', 'gateway', 'attribute', 'value', 'confirmed')
        read_only_fields = ('id',)

class MeasurementTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeasurementType
        fields = ('measurementTypeID', 'name', 'unit', 'scalar', 'upper_bound', 'lower_bound', 'alerts')
        read_only_fields = ('measurementTypeID',)

class GatewaySerializer(serializers.ModelSerializer):
    sensors = SensorSerializer(many=True, read_only=True)
    #sensors = serializers.PrimaryKeyRelatedField(many=True, queryset=Sensor.objects.all())
    #config = serializers.PrimaryKeyRelatedField(many=True, queryset=GatewayConfiguration.objects.all())
    config = GatewayConfigurationSerializer(many=True, read_only=True)

    alerts = AlertSerializer(many=True, read_only=True)

    measurement_types = MeasurementTypeSerializer(many=True, read_only=True)

    class Meta:
        model = Gateway
        # fields = ('gateway_id', 'sensors', 'installation', 'config', 'api_key')
        fields = ('gateway_id', 'sensors', 'installation', 'config', 'alerts', 'api_key', 'measurement_types')
        read_only_fields = ('gateway_id',)


class InstallationSerializer(serializers.ModelSerializer):
    #gateways = serializers.PrimaryKeyRelatedField(many=True, queryset=Gateway.objects.all())
    gateways = GatewaySerializer(many=True, read_only=True)

    class Meta:
        model = Installation
        #fields = ('installation_id', 'name', 'gateways', )
        #fields = '__all__'
        exclude = ('storage_on_remote', 'remote_database_id')
        read_only_fields = ('installation_id',)

class CompanySerializer(serializers.ModelSerializer):
    #installations = serializers.PrimaryKeyRelatedField(many=True, queryset=Gateway.objects.all())
    installations = InstallationSerializer(many=True, read_only=True)

    alerts = AlertSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ('company_id', 'name', 'installations', 'active', 'alerts', 'not_archived')
        read_only_fields = ('company_id',)


class MeasurementSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(MeasurementSerializer, self).__init__(many=many, *args, **kwargs)

    class Meta:
        model = Measurement
        fields = ('measurement_id', 'sensor_id', 'timestamp', 'measurement_type', 'value', 'alert')


class LiteMeasurementSerializer(serializers.ModelSerializer):
    #def __init__(self, *args, **kwargs):
    #    many = kwargs.pop('many', True)
    #    super(LiteMeasurementSerializer, self).__init__(many=many, *args, **kwargs)

    class Meta:
        model = Measurement
        fields = ('timestamp', 'value')


class TemplateParameterSerializer(serializers.ModelSerializer):

    class Meta:
        model = TemplateParameter
        fields = ('attribute', 'value')

class TemplateSerializer(serializers.ModelSerializer):
    params = TemplateParameterSerializer(many=True, read_only=True)

    class Meta:
        model = Template
        fields = ('template_id', 'name', 'entityType', 'params')
