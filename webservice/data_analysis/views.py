from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic

from data_analysis.models import Company, Installation, Gateway, Sensor


class IndexView(generic.ListView):
    template_name = 'data_analysis/index.html'

    def get_queryset(self):
        return


def companyView(request):  # This will become a form handler class to handle login
    company_list = Company.objects.all()
    context = {'company_list': company_list}
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return render(request, 'data_analysis/company.html', context)


class CompanyDetailView(generic.DetailView):
    model = Company
    template_name = 'data_analysis/company_detail.html'


class InstallationDetailView(generic.DetailView):
    model = Installation
    template_name = 'data_analysis/installation_detail.html'


class GatewayDetailView(generic.DetailView):
    model = Gateway
    template_name = 'data_analysis/gateway_detail.html'


class SensorDetailView(generic.DetailView):
    model = Sensor
    template_name = 'data_analysis/sensor_detail.html'
