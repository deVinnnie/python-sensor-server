from django.shortcuts import get_object_or_404, render, redirect
from datetime import datetime
from data.models import Company, Installation, Gateway, Sensor, Alert, MeasurementType
from django.db.models import Max


def alerts(request):
    """""
    Determine Alerts
    """""
    measurement_types = MeasurementType.objects.all()
    for t in measurement_types:
        min = t.lower_bound
        max = t.upper_bound

        set = Sensor.objects.all()
        for s in set:
            # dangers = s.measurements.filter(value__gte=10)
            # dangers = dangers.filter(value__lte=10)

            max_timestamp = s.measurements.aggregate(Max('timestamp'))['timestamp__max']
            if s.last_check != None:
                dangers = s.measurements.filter(measurement_type__exact=t.measurementTypeID, timestamp__gt = s.last_check)
            else:
                dangers = s.measurements.filter(measurement_type__exact=t.measurementTypeID)
            the_dangers = dangers.filter(value__gte=max) | dangers.filter(value__lte=min)

            for m in the_dangers:
                company = m.sensor_id.gateway.installation.company.company_id
                gateway = m.sensor_id.gateway.gateway_id
                sensor = m.sensor_id.tag
                Alert.objects.create(text="Sensor " + sensor + " has a measurement out of bounds! (" + t.name + ")",
                                     archived=0,
                                     company=Company.objects.get(pk=company),
                                     sensor=Sensor.objects.get(pk=m.sensor_id.sensor_id),
                                     measurement=m)
                break

            s.last_check = max_timestamp
            s.save()

    return redirect('company-list')