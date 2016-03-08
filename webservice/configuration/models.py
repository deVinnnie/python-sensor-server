from django.db import models

class SensorConfiguration(models.Model):
    sensor = models.ForeignKey('data.Sensor', db_column='Sensor_ID', related_name='config')  # Field name made lowercase.
    attribute = models.CharField(db_column='Attribute', max_length=45)
    value = models.CharField(db_column='Value', max_length=200, blank=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Sensor_Configuration'
        unique_together = ('sensor', 'attribute')

    def __str__(self):
        return self.sensor

class GatewayConfiguration(models.Model):
    gateway = models.ForeignKey('data.Gateway', db_column='Gateway_ID', related_name='config')  # Field name made lowercase.
    attribute = models.CharField(db_column='Attribute', max_length=45)  # Field name made lowercase.
    value = models.CharField(db_column='Value', max_length=200, blank=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Gateway_Configuration'
        unique_together = ('gateway', 'attribute')

    def __str__(self):
        return self.gateway
