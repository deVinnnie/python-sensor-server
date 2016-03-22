from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import status, permissions, views, renderers, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from data.models import *
from rest.serializers import *
from datetime import datetime

from .custom_renderers import *


# Note on PUT requests:
#
# Make sure you include an 'update' view when making a put-request.
# Without an update view the request will return the HTTP 500 error code
# and reload the current page (which may be what you wanted, but it's not the way to do it)
#

class HTMLGenericViewSet():
    """
    Generic class implementing the get_template_names() method.
    This is used for viewsets to define explicit templates per action,
    without manually overriding each action.
    """
    renderer_classes = (renderers.JSONRenderer,
                        renderers.TemplateHTMLRenderer,
                        renderers.BrowsableAPIRenderer
                        )

    def get_template_names(self):
        meta = self.get_queryset().model._meta
        #app = meta.app_label
        app = 'data'
        name = meta.object_name.lower()

        templates = {
            'list': ["%s/%s-list.html" % (app, name), "list.html"],
            'retrieve': ["%s/%s-detail.html" % (app, name), "detail.html"],

            'create': ["%s/%s-created.html" % (app, name), "created.html"],
            #'create': ["%s/%s-detail.html" % (app, name), "created.html"], #Redirect?
            'edit': ["%s/%s-update.html" % (app, name), "update.html"],
            'update': ["%s/%s-update.html" % (app, name), "update.html"],
            'delete': ["%s/%s-destroy.html" % (app, name), "destroy.html"],

            'new' : ["%s/%s-new.html" % (app, name), "new.html"],

        }


        print("D")
        print(self.action)
        if self.action in templates.keys():
            selected_templates = templates[self.action]
        else:
            selected_templates = ['rest_framework/api.html']

        return selected_templates


class CompanyViewSet(viewsets.ModelViewSet, HTMLGenericViewSet):
    """
    /companies
    """
    renderer_classes = HTMLGenericViewSet.renderer_classes
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (permissions.IsAuthenticated,)

    @list_route(methods=['get'])
    def new(self, request):
        return Response()

    @detail_route(methods=['get'])
    def new_installation(self, request, pk=None):
        """
        Loads data/company_new_installation.html which contains a form to add a new installation.
        This form does a POST request to /rest/installations/ to add the installation.
        """
        company = get_object_or_404(self.queryset, pk=pk)
        serializer = CompanySerializer(company)
        return Response(serializer.data,template_name='data/company_new_installation.html')


    @detail_route(methods=['get'])
    def deactivate(self, request, pk=None):
        company = get_object_or_404(self.queryset, pk=pk)
        company.active = False
        company.save()
        return redirect('company-detail', pk)

    @detail_route(methods=['get'])
    def activate(self, request, pk=None):
        company = get_object_or_404(self.queryset, pk=pk)
        company.active = True
        company.save()
        return redirect('company-detail', pk)


class InstallationViewSet(viewsets.ModelViewSet, HTMLGenericViewSet):
    """
    /installations/

    To create a new Installation: POST JSON or Form data to /rest/installations/
    This method is not explicitly defined, but is provided by the ModelViewSet class.
    A POST request will be handled by the list method (defined in ModelViewSet, the super class).
    See http://www.django-rest-framework.org/api-guide/viewsets/
    """
    renderer_classes = HTMLGenericViewSet.renderer_classes
    queryset = Installation.objects.all()
    serializer_class = InstallationSerializer

    @detail_route(methods=['get'])
    def add_gateway(self, request, pk=None):
        installation = get_object_or_404(self.queryset, pk=pk)
        serializer = InstallationSerializer(installation)
        return Response(serializer.data,template_name='data/installation-add_gateway.html')

    @detail_route(methods=['get'])
    def deactivate(self, request, pk=None):
        company = get_object_or_404(self.queryset, pk=pk)
        company.active = False
        company.save()
        return redirect('company-detail', pk)

    @detail_route(methods=['get'])
    def activate(self, request, pk=None):
        company = get_object_or_404(self.queryset, pk=pk)
        company.active = True
        company.save()
        return redirect('company-detail', pk)


class GatewayViewSet(viewsets.ModelViewSet, HTMLGenericViewSet):
    """
    /gateways
    """
    renderer_classes = HTMLGenericViewSet.renderer_classes
    queryset = Gateway.objects.all()
    serializer_class = GatewaySerializer

    @detail_route(methods=['get'])
    def new_config(self, request, pk=None):
        """
        Loads data/company_new_installation.html which contains a form to add a new installation.
        This form does a POST request to /rest/installations/ to add the installation.
        """
        gateway = get_object_or_404(self.queryset, pk=pk)
        serializer = GatewaySerializer(gateway)
        return Response(serializer.data,template_name='data/gateway_new_config.html')


class GatewayConfigurationViewSet(viewsets.ModelViewSet,HTMLGenericViewSet):
    """
    /gateways/$1/config
    """
    #renderer_classes = (RawConfigJSONRenderer,) + HTMLGenericViewSet.renderer_classes
    renderer_classes = HTMLGenericViewSet.renderer_classes
    queryset = GatewayConfiguration.objects.all()
    serializer_class = GatewayConfigurationSerializer

    def list(self, request, gateway_pk=None, format=None):
        """
        Returns data in following format:
        {
            "interval" : "12",
            "data-scheme" : "xsd:dfsfdf",
            ....
        }
        """
        queryset = self.queryset.filter(gateway=gateway_pk)
        serializer = GatewayConfigurationSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, gateway_pk=None, pk=None, format=None):
        queryset = get_object_or_404(self.queryset, id=pk)
        serializer = GatewayConfigurationSerializer(queryset)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def deactivate(self, request, gateway_pk=None, pk=None):
        gatewayConf = get_object_or_404(self.queryset, id=pk)
        gatewayConf.deleted = True
        gatewayConf.save()
        return redirect('gateway-detail', gateway_pk)

    @detail_route(methods=['get'])
    def edit(self, request, gateway_pk=None, pk=None,format=None):
        gatewayConf = get_object_or_404(self.queryset, id=pk)
        serializer = GatewayConfigurationSerializer(gatewayConf)



        # if serializer.is_valid():
        #     serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK, template_name='data/gateway-update.html')
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SensorViewSet(viewsets.ModelViewSet):
    """
    /gateways/$1/sensors
    """
    renderer_classes = HTMLGenericViewSet.renderer_classes
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    def list(self, request, companies_pk=None, installation_pk=None, gateway_pk=None, sensor_pk=None, format=None):
        queryset = self.queryset.filter(gateway_id=gateway_pk)
        serializer = SensorSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, companies_pk=None, installation_pk=None, gateway_pk=None, pk=None, format=None):
        queryset = get_object_or_404(self.queryset, sensor_id=pk)
        serializer = SensorSerializer(queryset)
        return Response(serializer.data)

    def create(self, request, companies_pk=None, installation_pk=None, gateway_pk=None, pk=None, format=None, *args, **kwargs):
        request.data['gateway'] = gateway_pk
        return super(SensorViewSet, self).create(request, *args, **kwargs)


class MeasurementViewSet(
                        mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet,
                        HTMLGenericViewSet):
    """
    /gateways/$1/sensors/$2/measurements/

    Example creating multiple entities in one request.
    {
        "measurements" :
        [
        {
            "sensor_id": 4,
            "timestamp": "2015-10-10T10:00:00",
            "measurement_type": 0,
            "value": 42.96
        },
        {
            "sensor_id": 4,
            "timestamp": "2015-10-10T11:00:00",
            "measurement_type": 0,
            "value": 96.42
        }
        ]
    }
    """
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    renderer_classes = (RawMeasurementJSONRenderer,) + HTMLGenericViewSet.renderer_classes

    def list(self, request, gateway_pk=None, sensor_pk=None, format=None):
        """
        GET Request Filtering:
        /gateways/$1/sensors/$2/measurements?start=2015-01-01&end=2015-02-01&type=0
        Returns only measurement from sensor with ID $2 which have a timestamp that is in the range start -> end.
        type= measurement type
        """
        type = self.request.query_params.get('type', 0)

        queryset = self.queryset.filter(sensor_id=sensor_pk)
        queryset = queryset.filter(measurement_type=type)

        startTimestamp = self.request.query_params.get('start', "2000-01-01")
        startDate = datetime.strptime(startTimestamp, "%Y-%m-%d")

        endTimestamp = self.request.query_params.get('end', "2020-01-01")
        endDate = datetime.strptime(endTimestamp, "%Y-%m-%d")

        if startDate is not None:
            queryset = queryset.filter(timestamp__gte=startDate)

        if endDate is not None:
            queryset = queryset.filter(timestamp__lte=endDate)

        serializer = MeasurementSerializer(queryset, many=True)
        return Response( {'measurements': serializer.data})


    def retrieve(self, request, gateway_pk=None, sensor_pk=None, pk=None, format=None):
        queryset = get_object_or_404(self.queryset, sensor_id=sensor_pk, measurement_id=pk)
        serializer = MeasurementSerializer(queryset)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Overrides default create method to enable the creation
        of multiple measurement entities in one request.

        :param request:
            Must be encoded in the following way:
                {
                    "measurements" :
                    [
                    {
                        "sensor_id": 4,
                        "timestamp": "2015-10-10T10:00:00",
                        "measurement_type": 0,
                        "value": 42.96
                    },
                    {
                        "sensor_id": 4,
                        "timestamp": "2015-10-10T11:00:00",
                        "measurement_type": 0,
                        "value": 96.42
                    }
                    ]
                }
        """
        listOfThings = request.data['measurements']

        serializer = self.get_serializer(data=listOfThings, many=True)
        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED,
                            headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LiteMeasurementView(views.APIView):
    permission_classes = []

    def get(self, request, format=None, *args, **kwargs):
        # email = request.DATA.get('email', None)
        # url = request.DATA.get('url', None)
        return Response({"success": True})


class SensorConfigurationViewSet(viewsets.ModelViewSet, HTMLGenericViewSet):
    """
    /gateways/$1/sensors/$2/config
    """
    queryset = SensorConfiguration.objects.all()
    serializer_class = SensorConfigurationSerializer
    renderer_classes = HTMLGenericViewSet.renderer_classes

    def list(self, request, gateway_pk=None, sensor_pk=None, format=None):
        queryset = self.queryset.filter(sensor=sensor_pk)
        serializer = SensorConfigurationSerializer(queryset, many=True)
        return Response(serializer.data)

class MeasurementTypeViewSet(viewsets.ModelViewSet, HTMLGenericViewSet):
    """
    /measurement-type
    """
    queryset=MeasurementType.objects.all()
    serializer_class = MeasurementTypeSerializer
    renderer_classes = HTMLGenericViewSet.renderer_classes
