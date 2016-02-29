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

from django.db import models

class Company(models.Model):
    company_id = models.AutoField(db_column='Company_ID', primary_key=True)
    name = models.CharField(db_column='Name', max_length=45, blank=True) # Field name made lowercase.
    class Meta:
        managed = True
        db_table = 'Company'
    def __str__(self):
        return self.name

class Gateway(models.Model):
    gateway_id = models.IntegerField(db_column='Gateway_ID', primary_key=True) # Field name made lowercase.
    installation = models.ForeignKey('Installation', db_column='Installation_ID', blank=True, null=True, related_name="gateways") # Field name made lowercase.
    ip_address = models.CharField(db_column='IP-address', max_length=45, blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    class Meta:
        managed = True
        db_table = 'Gateway'
    def __str__(self):
        return 'Gateway ' +  repr(self.gateway_id)

class GatewayConfiguration(models.Model):
    gateway = models.ForeignKey(Gateway, db_column='Gateway_ID', related_name='config') # Field name made lowercase.
    attribute = models.CharField(db_column='Attribute', max_length=45, primary_key=True) # Field name made lowercase.
    value = models.CharField(db_column='Value', max_length=200, blank=True) # Field name made lowercase.
    class Meta:
        managed = True
        db_table = 'Gateway_Configuration'
    def __str__(self):
        return self.gateway

class Installation(models.Model):
    installation_id = models.IntegerField(db_column='Installation_ID', primary_key=True) # Field name made lowercase.
    company = models.ForeignKey(Company, db_column='Company_ID', related_name='installations') # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=45, blank=True) # Field name made lowercase.
    storage_on_remote = models.IntegerField(db_column='Storage_On_Remote') # Field name made lowercase.
    remote_database_id = models.IntegerField(db_column='Remote_Database_ID', blank=True, null=True) # Field name made lowercase.
    class Meta:
        managed = True
        db_table = 'Installation'
    def __str__(self):
        return self.name
        
class Sensor(models.Model):
    sensor_id = models.IntegerField(db_column='Sensor_ID', primary_key=True) # Field name made lowercase.
    gateway_id = models.ForeignKey(Gateway, db_column='Gateway_ID', related_name='sensors', default="1") # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=45, blank=True) # Field name made lowercase.
    position_long = models.DecimalField(db_column='Position_Long', max_digits=10, decimal_places=0, blank=True, null=True) # Field name made lowercase.
    position_lat = models.DecimalField(db_column='Position_Lat', max_digits=10, decimal_places=0, blank=True, null=True) # Field name made lowercase.
    class Meta:
        managed = True
        db_table = 'Sensor'
    def __str__(self):
        return 'Sensor ' + repr(self.sensor_id)

    def measurement_types(self):
        #print(self.measurements.values('measurement_type'))
        return (0,1,2)

class MeasurementType(models.Model):
    measurementTypeID = models.IntegerField(db_column='MeasurementTypeID', primary_key=True) # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=45, blank=True) # Field name made lowercase.
    scalar = models.IntegerField(db_column='Scalar', blank=True, null=True) # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=45, blank=True) # Field name made lowercase.
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
    value = models.DecimalField(db_column='Value', max_digits=10, decimal_places=5, blank=True, null=True) # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Measurement'
    def total_value(self):
        return self.value * self.measurement_type.scalar
    def __str__(self):
        return '{:%Y-%m-%d %H:%M:%S}'.format(self.timestamp)

class Permission(models.Model):
    permission_id = models.IntegerField(db_column='Permission_ID', primary_key=True) # Field name made lowercase.
    entity = models.CharField(db_column='Entity', max_length=45) # Field name made lowercase.
    identifier = models.CharField(db_column='Identifier', max_length=45) # Field name made lowercase.
    action = models.CharField(db_column='Action', max_length=45) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'Permission'

class RemoteDatabase(models.Model):
    remote_database_id = models.IntegerField(db_column='Remote_Database_ID', primary_key=True) # Field name made lowercase.
    url = models.CharField(db_column='URL', max_length=300, blank=True) # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=45, blank=True) # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=45, blank=True) # Field name made lowercase.
    class Meta:
        managed = True
        db_table = 'Remote_Database'


class SensorConfiguration(models.Model):
    sensor = models.ForeignKey(Sensor, db_column='Sensor_ID', related_name='config') # Field name made lowercase.
    attribute = models.CharField(max_length=45, primary_key=True)
    value = models.CharField(db_column='Value', max_length=200, blank=True) # Field name made lowercase.
    class Meta:
        managed = True
        db_table = 'Sensor_Configuration'
        
        
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
