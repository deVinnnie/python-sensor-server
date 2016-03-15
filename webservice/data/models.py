# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals
from django.template.loader import render_to_string

from django.core.urlresolvers import reverse

from django.db import models
from django.db.models import Count
from .fields import UUIDField

class Company(models.Model):
    company_id = models.AutoField(db_column='Company_ID', primary_key=True)
    name = models.CharField(db_column='Name', max_length=45, blank=True)  # Field name made lowercase.
    active = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'Company'

    def get_absolute_url(self):
        return reverse('data:company_detail', args=[str(self.company_id)])

    def __str__(self):
        return self.name


class Installation(models.Model):
    installation_id = models.AutoField(db_column='Installation_ID', primary_key=True)
    company = models.ForeignKey(Company, db_column='Company_ID', related_name='installations')
    name = models.CharField(db_column='Name', max_length=45, blank=True)
    storage_on_remote = models.IntegerField(db_column='Storage_On_Remote', blank=True, default=0)
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
    gateway_id = models.AutoField(db_column='Gateway_ID', primary_key=True)  # Field name made lowercase.
    installation = models.ForeignKey(Installation, db_column='Installation_ID', blank=True, null=True,
                                     related_name="gateways")  # Field name made lowercase.
    ip_address = models.CharField(db_column='IP-address', max_length=45,
                                  blank=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    active = models.BooleanField(default=True)

    api_key = UUIDField()#auto=True)

    class Meta:
        managed = True
        db_table = 'Gateway'

    def get_absolute_url(self):
        return reverse('data:gateway_detail',
                       args=[str(self.installation.company.company_id), str(self.installation.installation_id),
                             str(self.gateway_id)])

    def __str__(self):
        return 'Gateway ' + repr(self.gateway_id)


class Sensor(models.Model):
    sensor_id = models.AutoField(db_column='Sensor_ID', primary_key=True)  # Field name made lowercase.
    gateway = models.ForeignKey(Gateway, db_column='Gateway_ID', related_name='sensors',
                                default="1")  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=45, blank=True,
                            default='Sensor Node')  # Field name made lowercase.
    position_long = models.DecimalField(db_column='Position_Long', max_digits=10, decimal_places=0, blank=True,
                                        null=True)  # Field name made lowercase.
    position_lat = models.DecimalField(db_column='Position_Lat', max_digits=10, decimal_places=0, blank=True,
                                       null=True)  # Field name made lowercase.

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
    measurementTypeID = models.IntegerField(db_column='MeasurementTypeID', primary_key=True)
    unit = models.CharField(db_column='Unit', max_length=45, blank=True)
    scalar = models.IntegerField(db_column='Scalar', blank=True, null=True)
    name = models.CharField(db_column='Name', max_length=45, blank=True)

    class Meta:
        managed = True
        db_table = 'MeasurementType'

    def __str__(self):
        return self.name


class Measurement(models.Model):
    measurement_id = models.AutoField(db_column='Measurement_ID', primary_key=True) # Field name made lowercase.
    timestamp = models.DateTimeField(db_column='Timestamp') # Field name made lowercase.
    sensor_id = models.ForeignKey(Sensor, db_column='Sensor_ID', related_name='measurements') # Field name made lowercase.
    measurement_type = models.ForeignKey(MeasurementType, db_column='Measurement_Type') # Field name made lowercase.
    value = models.FloatField(db_column='Value', blank=True, null=True) # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Measurement'

    def total_value(self):
        return self.value * self.measurement_type.scalar

    def __str__(self):
        return '{:%Y-%m-%d %H:%M:%S}'.format(self.timestamp)


class RemoteDatabase(models.Model):
    remote_database_id = models.IntegerField(db_column='Remote_Database_ID',
                                             primary_key=True)  # Field name made lowercase.
    url = models.CharField(db_column='URL', max_length=300, blank=True)  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=45, blank=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=45, blank=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Remote_Database'


class SensorConfiguration(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    sensor = models.ForeignKey(Sensor, db_column='Sensor_ID', related_name='config')  # Field name made lowercase.
    attribute = models.CharField(db_column='Attribute', max_length=45)
    value = models.CharField(db_column='Value', max_length=200, blank=True)  # Field name made lowercase.
    confirmed = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'Sensor_Configuration'
        unique_together = ('sensor', 'attribute')

    def __str__(self):
        return self.sensor


class GatewayConfiguration(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    gateway = models.ForeignKey(Gateway, db_column='Gateway_ID', related_name='config')  # Field name made lowercase.
    attribute = models.CharField(db_column='Attribute', max_length=45)  # Field name made lowercase.
    value = models.CharField(db_column='Value', max_length=200, blank=True)  # Field name made lowercase.
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
    url = models.URLField()
    company = models.ForeignKey(Company, related_name='alerts')
    archived = models.BooleanField(default=False)

# class Permission(models.Model):
#     permission_id = models.IntegerField(db_column='Permission_ID', primary_key=True) # Field name made lowercase.
#     entity = models.CharField(db_column='Entity', max_length=45) # Field name made lowercase.
#     identifier = models.CharField(db_column='Identifier', max_length=45) # Field name made lowercase.
#     action = models.CharField(db_column='Action', max_length=45) # Field name made lowercase.
#     class Meta:
#         managed = False
#         db_table = 'Permission'

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
