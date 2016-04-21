from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic

from data.models import Company, Installation, Gateway, Sensor, Alert, MeasurementType

def alerts(request):
    """
    Determine Alerts
    """
    measurement_types = MeasurementType.objects.all()
    for t in measurement_types:
        min = t.lower_bound
        max = t.upper_bound

        set = Sensor.objects.all()
        for s in set:
            # dangers = s.measurements.filter(value__gte=10)
            # dangers = dangers.filter(value__lte=10)
            #min = 0
            #max = 27.7
            dangers = s.measurements.filter(measurement_type__exact=t.measurementTypeID)
            the_dangers = dangers.filter(value__gte=max) | dangers.filter(value__lte=min)


            for m in the_dangers:
                if m.alert == False:
                    print(m.value)
                    company = m.sensor_id.gateway.installation.company.company_id
                    gateway = m.sensor_id.gateway.gateway_id
                    sensor = m.sensor_id.sensor_id
                    Alert.objects.create(text="Sensor " + str(sensor) + " has a measurement out of bounds! (" + t.name + ")", url="", archived=0,
                                         company=Company.objects.get(pk=company),
                                         gateway=Gateway.objects.get(pk=gateway),
                                         sensor=Sensor.objects.get(pk=sensor),
                                         measurementTypeID=MeasurementType.objects.get(pk=1))
                    m.alert = True
                    m.save()

            # for m in dangers2:
            #     if m.alert == False:
            #         print(m.value)
            #         company = m.sensor_id.gateway.installation.company.company_id
            #         gateway = m.sensor_id.gateway.gateway_id
            #         sensor = m.sensor_id.sensor_id
            #         Alert.objects.create(text="Sensor " + str(sensor) + " has a measurement out of bounds! (" + t.name + ")", url="", archived=0,
            #                              company=Company.objects.get(pk=company),
            #                              gateway=Gateway.objects.get(pk=gateway),
            #                              sensor=Sensor.objects.get(pk=sensor))
            #         m.alert = True
            #         m.save()

    return redirect('company-list')