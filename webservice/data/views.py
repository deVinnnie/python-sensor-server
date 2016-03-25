from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic

from data.models import Company, Installation, Gateway, Sensor, Alert, MeasurementType


class IndexView(generic.ListView):
    template_name = 'data/index.html'

    def get_queryset(self):
        return


def companyView(request):  # This will become a form handler class to handle login
    company_list = Company.objects.all()
    context = {'company_list': company_list}
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return render(request, 'data/company.html', context)


class CompanyDetailView(generic.DetailView):
    model = Company
    template_name = 'data/company-detail.html'


class InstallationDetailView(generic.DetailView):
    model = Installation
    template_name = 'data/installation-detail.html'


class GatewayDetailView(generic.DetailView):
    model = Gateway
    template_name = 'data/gateway_detail.html'


class SensorDetailView(generic.DetailView):
    model = Sensor
    template_name = 'data/sensor_detail.html'


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
            dangers1 = dangers.filter(value__gte=max)
            dangers2 = dangers.filter(value__lte=min)
            for m in dangers1:
                if m.alert == False:
                    print(m.value)
                    company = m.sensor_id.gateway.installation.company.company_id
                    gateway = m.sensor_id.gateway.gateway_id
                    sensor = m.sensor_id.sensor_id
                    Alert.objects.create(text="Sensor " + str(sensor) + " has a measurement out of bounds!", url="", archived=0,
                                         company=Company.objects.get(pk=company),
                                         gateway=Gateway.objects.get(pk=gateway),
                                         sensor=Sensor.objects.get(pk=sensor))
                    m.alert = True
                    m.save()

            for m in dangers2:
                if m.alert == False:
                    print(m.value)
                    Alert.objects.create(text="Sensor " + str(sensor) + " has a measurement out of bounds!", url="", archived=0,
                                         company=Company.objects.get(pk=company),
                                         gateway=Gateway.objects.get(pk=gateway),
                                         sensor=Sensor.objects.get(pk=sensor))
                    m.alert = True
                    m.save()


    # return HttpResponse("Hello, world. You're at the polls index.")
    return redirect('company-list')