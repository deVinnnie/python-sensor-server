from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic

from data.models import Company, Installation, Gateway, Sensor, Alert


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
    # set = Sensor.objects.all()
    s = Sensor.objects.get(pk=1)
    # for s in set:
        # dangers = s.measurements.filter(value__gte=10)
        # dangers = dangers.filter(value__lte=10)
    min = 0
    max = 23
    dangers = s.measurements.filter(measurement_type__exact=1)
    dangers1 = dangers.filter(value__gte=max)
    dangers2 = dangers.filter(value__lte=min)
    for m in dangers1:
        print(m.value)
        Alert.objects.create(text="Automatic Alert Test", url="", archived=0, company=Company.objects.get(pk=1),
                             gateway=Gateway.objects.get(pk=1),
                             sensor=Sensor.objects.get(pk=1))

    for m in dangers2:
        print(m.value)
        Alert.objects.create(text="Automatic Alert Test", url="", archived=0, company=Company.objects.get(pk=1),
                             gateway=Gateway.objects.get(pk=1),
                             sensor=Sensor.objects.get(pk=1))


    return HttpResponse("Hello, world. You're at the polls index.")