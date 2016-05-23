from rest_framework import serializers
from data.models import *

class MeasurementTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeasurementType
        fields = ('measurementTypeID', 'name', 'unit', 'scalar', 'upper_bound', 'lower_bound')#, 'alerts')
        read_only_fields = ('measurementTypeID',)


class MeasurementSerializer(serializers.ModelSerializer):
    measurement_type = MeasurementTypeSerializer()

    class Meta:
        model = Measurement
        fields = ('measurement_id', 'timestamp', 'measurement_type', 'value')

class MeasurementCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ('measurement_id', 'sensor_id', 'timestamp', 'measurement_type', 'value')


class AlertSerializer(serializers.ModelSerializer):
    measurement = MeasurementSerializer(read_only=True)

    class Meta:
        model = Alert
        fields = ('id', 'text', 'company', 'archived', 'sensor', 'measurement')
        read_only_fields = ('id', 'text', 'company', 'sensor')


class SensorConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorConfiguration
        fields = ('sensor', 'gateway', 'id', 'attribute', 'value', 'confirmed')


class SensorSerializer(serializers.ModelSerializer):
    config = SensorConfigurationSerializer(many=True, read_only=True)
    alerts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Sensor
        fields = ('sensor_id', 'tag', 'config', 'position_long', 'position_lat', 'alerts')
        read_only_fields = ('sensor_id')


class GatewayConfigurationSerializer(serializers.ModelSerializer):

    class Meta:
        model = GatewayConfiguration
        fields = ('id', 'gateway', 'attribute', 'value', 'confirmed')
        read_only_fields = ('id',)


class GatewaySerializer(serializers.ModelSerializer):
    sensors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    config = GatewayConfigurationSerializer(many=True, read_only=True)
    alerts = AlertSerializer(many=True, read_only=True)
    measurement_types = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Gateway
        fields = ('gateway_id', 'sensors', 'installation', 'config', 'alerts', 'api_key', 'measurement_types')
        read_only_fields = ('gateway_id',)


class InstallationSerializer(serializers.ModelSerializer):
    gateways = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Installation
        exclude = ('storage_on_remote', 'remote_database_id')
        read_only_fields = ('installation_id',)


class CompanySerializer(serializers.ModelSerializer):
    installations = InstallationSerializer(many=True, read_only=True)
    #alerts = AlertSerializer(many=True, read_only=True)
    active_alerts = AlertSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ('company_id', 'name', 'installations', 'active', 'active_alerts')
        read_only_fields = ('company_id',)


class LiteMeasurementSerializer(serializers.ModelSerializer):
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
