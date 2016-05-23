from __future__ import unicode_literals
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
from .fields import UUIDField
import uuid


class Company(models.Model):
    company_id = models.AutoField(db_column='Company_ID', primary_key=True)
    name = models.CharField(db_column='Name', max_length=45, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'Company'

    def get_absolute_url(self):
        return reverse('data:company_detail', args=[str(self.company_id)])

    def __str__(self):
        return self.name

    def active_alerts(self):
         return self.alerts.filter(archived=False)


class Installation(models.Model):
    installation_id = models.AutoField(db_column='Installation_ID', primary_key=True)
    company = models.ForeignKey(Company, db_column='Company_ID', related_name='installations')
    name = models.CharField(db_column='Name', max_length=45, blank=True)
    storage_on_remote = models.BooleanField(db_column='Storage_On_Remote', default=False)
    remote_database_id = models.IntegerField(db_column='Remote_Database_ID', blank=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'Installation'

    def get_absolute_url(self):
        return reverse('data:installation_detail',
                       args=[str(self.company.company_id), str(self.installation_id)])

    def __str__(self):
        return self.name


class Gateway(models.Model):
    gateway_id = models.AutoField(db_column='Gateway_ID', primary_key=True)
    installation = models.ForeignKey(Installation, db_column='Installation_ID', blank=True, null=True,
                                     related_name="gateways")
    active = models.BooleanField(default=True)

    api_key = UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        managed = True
        db_table = 'Gateway'

    def get_absolute_url(self):
        return reverse('data:gateway_detail',
                       args=[str(self.installation.company.company_id),
                             str(self.installation.installation_id),
                             str(self.gateway_id)])

    def __str__(self):
        return 'Gateway ' + repr(self.gateway_id)

    def measurement_types(self):
        """
        Return all available measurement types
        """
        return MeasurementType.objects.all()


class Sensor(models.Model):
    sensor_id = models.AutoField(db_column='Sensor_ID', primary_key=True)
    gateway = models.ForeignKey(Gateway, db_column='Gateway_ID', related_name='sensors', default="1")
    tag = models.CharField(db_column='Name', max_length=45, blank=True, default='Sensor Node')
    position_long = models.FloatField(db_column='Position_Long', blank=True, null=True)
    position_lat = models.FloatField(db_column='Position_Lat', blank=True, null=True)

    # Last time since measurements were checked for outliers and abnormalities.
    last_check = models.DateTimeField(db_column='Last_Check', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Sensor'

    def get_absolute_url(self):
        return reverse('data:sensor_detail', args=[str(self.gateway.installation.company.company_id),
                                                   str(self.gateway.installation.installation_id),
                                                   str(self.gateway.gateway_id), str(self.sensor_id)])

    def measurement_chart(self):
        return render_to_string('admin/data/sensor/measurement_chart.html')

    measurement_chart.allow_tags = True

    def __str__(self):
        return 'Sensor ' + repr(self.sensor_id)

    def measurement_types(self):
        set = Measurement.objects.values('measurement_type').annotate(c=Count('measurement_type')).values('measurement_type')
        resultSet = []
        for m in set:
            resultSet.append(m['measurement_type'])

        return resultSet


class MeasurementType(models.Model):
    measurementTypeID = models.AutoField(db_column='MeasurementTypeID', primary_key=True)
    unit = models.CharField(db_column='Unit', max_length=45, blank=True)
    scalar = models.IntegerField(db_column='Scalar', blank=True, null=True)
    name = models.CharField(db_column='Name', max_length=45, blank=True)
    upper_bound = models.IntegerField(default = 27)
    lower_bound = models.IntegerField(default = 0)

    class Meta:
        managed = True
        db_table = 'MeasurementType'

    def __str__(self):
        return self.name


class Measurement(models.Model):
    measurement_id = models.AutoField(db_column='Measurement_ID', primary_key=True)
    timestamp = models.DateTimeField(db_column='Timestamp')
    sensor_id = models.ForeignKey(Sensor, db_column='Sensor_ID', related_name='measurements')
    measurement_type = models.ForeignKey(MeasurementType, db_column='Measurement_Type')
    value = models.FloatField(db_column='Value', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Measurement'

    def total_value(self):
        return self.value * self.measurement_type.scalar

    def __str__(self):
        return '{:%Y-%m-%d %H:%M:%S}'.format(self.timestamp)


class SensorConfiguration(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    sensor = models.ForeignKey(Sensor, db_column='Sensor_ID', related_name='config')
    attribute = models.CharField(db_column='Attribute', max_length=45)
    value = models.CharField(db_column='Value', max_length=200, blank=True)
    confirmed = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'Sensor_Configuration'
        unique_together = ('sensor', 'attribute')

    def __str__(self):
        return self.sensor

    def gateway(self):
        return self.sensor.gateway_id


class GatewayConfiguration(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    gateway = models.ForeignKey(Gateway, db_column='Gateway_ID', related_name='config')
    attribute = models.CharField(db_column='Attribute', max_length=45)
    value = models.CharField(db_column='Value', max_length=200, blank=True)
    confirmed = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'Gateway_Configuration'
        unique_together = ('gateway', 'attribute')

    def __str__(self):
        return self.gateway


class Alert(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=500)
    company = models.ForeignKey(Company, related_name='alerts')
    archived = models.BooleanField(default=False)
    sensor = models.ForeignKey(Sensor, db_column='Sensor_ID', related_name='alerts')
    measurement = models.ForeignKey(Measurement, db_column='Measurement_ID', related_name='alert')

    def type_name(self):
        return self.measurement_type.name


class Permission(models.Model):
    permission_id = models.AutoField(db_column='Permission_ID', primary_key=True)
    entity = models.CharField(db_column='Entity', max_length=45)
    identifier = models.IntegerField(db_column='Identifier')
    action = models.CharField(db_column='Action', max_length=45)
    user = models.ForeignKey(User, db_column='User')

    class Meta:
        db_table = 'Permission'


class Template(models.Model):
    template_id = models.AutoField(db_column='Permission_ID', primary_key=True)
    name = models.CharField(max_length=45)
    entityType = models.CharField(max_length=100)

    class Meta:
        db_table = 'Template'


class TemplateParameter(models.Model):
    attribute = models.CharField(db_column='Attribute', max_length=45)
    value = models.CharField(db_column='Value', max_length=200, blank=True)
    template = models.ForeignKey(Template, related_name='params')



# Unused models:
# --------------
# class VagueMeasurement(models.Model):
#     id = models.AutoField(primary_key=True)
#     timestamp = models.DateTimeField(db_column='Timestamp')
#     sensor_id = models.ForeignKey(Sensor, db_column='Sensor_ID', related_name='overview_measurements')
#     measurement_type = models.ForeignKey(MeasurementType, db_column='Measurement_Type')
#     value = models.FloatField(db_column='Value', blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = 'VagueMeasurement'
#
#     def __str__(self):
#         return '{:%Y-%m-%d %H:%M:%S}'.format(self.timestamp)
#     class RemoteDatabase(models.Model):
#         remote_database_id = models.IntegerField(db_column='Remote_Database_ID', primary_key=True)
#         url = models.CharField(db_column='URL', max_length=300, blank=True)
#         username = models.CharField(db_column='Username', max_length=45, blank=True)
#         password = models.CharField(db_column='Password', max_length=45, blank=True)
#
#         class Meta:
#             managed = True
#             db_table = 'Remote_Database'

# 
# class Role(models.Model):
#     role_id = models.IntegerField(db_column='Role_ID', primary_key=True) # Field name made lowercase.
#     role_name = models.CharField(db_column='Role_Name', max_length=45) # Field name made lowercase.
#     class Meta:
#         managed = False
#         db_table = 'Role'
# 
# class RoleHasPermission(models.Model):
#     role = models.ForeignKey(Role, db_column='Role_ID', primary_key=True) # Field name made lowercase.
#     permission = models.ForeignKey(Permission, db_column='Permission_ID', primary_key=True) # Field name made lowercase.
#     class Meta:
#         managed = False
#         db_table = 'Role_has_Permission'
# 
# class User(models.Model):
#     user_id = models.IntegerField(db_column='User_ID', primary_key=True) # Field name made lowercase.
#     username = models.CharField(db_column='Username', max_length=45) # Field name made lowercase.
#     password = models.CharField(db_column='Password', max_length=45) # Field name made lowercase.
#     email = models.CharField(db_column='Email', max_length=300) # Field name made lowercase.
#     full_name = models.CharField(db_column='Full_Name', max_length=300) # Field name made lowercase.
#     class Meta:
#         managed = False
#         db_table = 'User'
# 
# class UserHasPermission(models.Model):
#     user = models.ForeignKey(User, db_column='User_ID', primary_key=True) # Field name made lowercase.
#     permission = models.ForeignKey(Permission, db_column='Permission_ID', primary_key=True) # Field name made lowercase.
#     class Meta:
#         managed = False
#         db_table = 'User_has_Permission'
# 
# class UserHasRole(models.Model):
#     user = models.ForeignKey(User, db_column='User_ID', primary_key=True) # Field name made lowercase.
#     role = models.ForeignKey(Role, db_column='Role_ID', primary_key=True) # Field name made lowercase.
#     class Meta:
#         managed = False
#         db_table = 'User_has_Role'
