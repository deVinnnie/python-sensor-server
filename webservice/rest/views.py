from _ast import arg
from _testcapi import raise_exception
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import status, permissions, views, renderers, viewsets
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from data.models import *
from rest.serializers import *
from datetime import datetime, timedelta
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .permissions import IsGatewayOrAuthenticated, IsUserAllowed
from .custom_renderers import *
from django.db.models import Avg

from django.http import HttpResponse

from django.contrib.auth.models import User

# Note on PUT requests:
#
# Make sure you include an 'update' view when making a put-request.
# Without an update view the request will return the HTTP 500 error code
# and reload the current page (which may be what you wanted, but it's not the way to do it)
#

class HTMLGenericViewSet(viewsets.ModelViewSet):
    """
    Generic class implementing the get_template_names() method.
    This is used for viewsets to define explicit templates per action,
    without manually overriding each action.
    """
    renderer_classes = (
        renderers.JSONRenderer,
        renderers.TemplateHTMLRenderer,
        renderers.BrowsableAPIRenderer
    )

    permission_classes = (IsGatewayOrAuthenticated, IsUserAllowed)

    def get_template_names(self):
        meta = self.get_queryset().model._meta
        app = 'data'
        name = meta.object_name.lower()

        templates = {
            'list': ["%s/%s-list.html" % (app, name), "list.html"],
            'retrieve': ["%s/%s-detail.html" % (app, name), "detail.html"],
            'create': ["%s/%s-created.html" % (app, name), "created.html"],
            'edit': ["%s/%s-update.html" % (app, name), "update.html"],
            'update': ["%s/%s-update.html" % (app, name), "update.html"],
            'partial_update' : ["%s/%s-update.html" % (app, name), "update.html"],
            'delete': ["%s/%s-destroy.html" % (app, name), "destroy.html"],
            'destroy': ["%s/%s-destroy.html" % (app, name), "destroy.html"],
            'new' : ["%s/%s-new.html" % (app, name), "new.html"],
        }

        if self.action in templates.keys():
            selected_templates = templates[self.action]
        else:
            selected_templates = ['rest_framework/api.html']

        return selected_templates

    def getQSet(self):
        return self.queryset


class CompanyViewSet(HTMLGenericViewSet):
    """
    /companies
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

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


class InstallationViewSet(HTMLGenericViewSet):
    """
    /installations/

    To create a new Installation: POST JSON or Form data to /rest/installations/
    This method is not explicitly defined, but is provided by the ModelViewSet class.
    A POST request will be handled by the create method (defined in ModelViewSet, the super class).
    See http://www.django-rest-framework.org/api-guide/viewsets/
    """
    queryset = Installation.objects.all()
    serializer_class = InstallationSerializer

    @detail_route(methods=['get'])
    def add_gateway(self, request, pk=None):
        """
        Load the create form for a new gateway.
        """
        installation = get_object_or_404(self.queryset, pk=pk)
        serializer = InstallationSerializer(installation)
        return Response(serializer.data,template_name='data/installation-add_gateway.html')

    @detail_route(methods=['get'])
    def deactivate(self, request, pk=None):
        entity = get_object_or_404(self.queryset, pk=pk)
        entity.active = False
        entity.save()
        return redirect('installation-detail', pk)

    @detail_route(methods=['get'])
    def activate(self, request, pk=None):
        entity = get_object_or_404(self.queryset, pk=pk)
        entity.active = True
        entity.save()
        return redirect('installation-detail', pk)


class GatewayViewSet(HTMLGenericViewSet):
    """
    /gateways
    """
    queryset = Gateway.objects.all()
    serializer_class = GatewaySerializer
    permission_classes = (IsGatewayOrAuthenticated, IsUserAllowed)

    @detail_route(methods=['get'])
    def new_config(self, request, pk=None):
        gateway = get_object_or_404(self.queryset, pk=pk)
        serializer = GatewaySerializer(gateway)
        return Response(serializer.data,template_name='data/gateway_new_config.html')

    def create(self, request, *args, **kwargs):
        result = super(GatewayViewSet, self).create(request, *args, **kwargs)

        templates = Template.objects.filter(entityType="gateway")
        serializer = TemplateSerializer(templates, many=True)
        result.data['templates'] = serializer.data

        return result

    @detail_route(methods=['get'])
    def measurements(self, request, pk=None, type=1,format=None):
        """
        Returns an overview of the measurements for a specific type.
        Gives one average value per sensor per day.

        Example JSON output:
        {
          "measurements": {
            "values": [
              {
                "data": [
                  3.14,
                  null,
                  null
                ],
                "date": "2016-05-01"
              },
              {
                "data": [
                  4.0,
                  null,
                  null
                ],
                "date": "2016-05-02"
              },
            ],
            "sensors": {
              "1": "G2S1",
              "2": "G2S2",
              "3": "G2S3",
              "4": "G2S4",
              ...
            }
        }

        'sensors' contains a mapping of sensor id to sensor tag.
        The id is a string value - though the database value is integer - this is a
        limitation of JSON which only allows strings as key.
        Furthermore the 'sensors' list serves as the header for the actual measurements.
        The index in the array for measurement corresponds to the index its sensor in the "sensors' list.
        A null value in the values array means that no data was found.
        """

        # Time is not important. Date is.
        # Pick measurements based on date.
        gateway = get_object_or_404(self.queryset, pk=pk)

        startTimestamp = self.request.query_params.get('start', "2016-05-01")
        startDate = datetime.strptime(startTimestamp, "%Y-%m-%d")

        endTimestamp = self.request.query_params.get('end', "2016-05-05")
        endDate = datetime.strptime(endTimestamp, "%Y-%m-%d")

        data = {}
        sensorList = {}

        for sensor in gateway.sensors.all():
            sensorList[sensor.sensor_id] = sensor.tag

        data["measurements"] = {
                            "sensors" : sensorList,
                            "values" : []
        }

        while(startDate != endDate):
            values = []
            for sensor in gateway.sensors.all():
                queryRes = sensor.measurements.filter(
                                    measurement_type=type, timestamp__gte=startDate,
                                    timestamp__lte=startDate + timedelta(days=1)
                                  ).aggregate(Avg('value'))
                average = queryRes["value__avg"]
                if average != None:
                    average = round(average, 2)
                values.append(average)

            data["measurements"]["values"].append({"date" : startDate.strftime("%Y-%m-%d"),"data" : values})
            startDate += timedelta(days=1)

        return Response(data)

    @detail_route(methods=['get'])
    def use_template(self, request, pk=None, *args, **kwargs):
        """
        Set the configuration parameters for this gateway based on a template.

        If keys in the template already exist, they will be overwritten with
        the template value.
        Keys with are present in the current configuration, but are absent from
        the template are left untouched.
        """
        gateway = get_object_or_404(self.queryset, pk=pk)

        template_id = request.GET['template_id']
        template = get_object_or_404(Template.objects.all(), pk=template_id)

        for param in template.params.all():
            if len(gateway.config.filter(attribute=param.attribute)) != 0:
                # Config with same attribute exists. Overwrite.
                conf = gateway.config.filter(attribute=param.attribute)[0]
                conf.value = param.value
                conf.save()
            else:
                # Add new.
                gateway.config.create(attribute=param.attribute, value=param.value)
        return redirect('gateway-detail', pk)


class GatewayConfigurationViewSet(HTMLGenericViewSet):
    """
    /gateways/$1/config
    """
    #renderer_classes = (RawConfigJSONRenderer,) + HTMLGenericViewSet.renderer_classes
    queryset = GatewayConfiguration.objects.all()
    serializer_class = GatewayConfigurationSerializer
    #permission_classes = (IsGatewayOrAuthenticated, IsUserAllowed,)

    def list(self, request, gateway_pk=None, format=None):
        """
        Returns data in following format (<Key, Value> pairs):
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
    def edit(self, request, gateway_pk=None, pk=None,format=None):
        gatewayConf = get_object_or_404(self.queryset, pk=pk)
        serializer = GatewayConfigurationSerializer(gatewayConf)

        # if serializer.is_valid():
        #     serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK, template_name='data/gateway-update.html')
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SensorViewSet(HTMLGenericViewSet):
    """
    /gateways/$1/sensors
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = (IsGatewayOrAuthenticated, IsUserAllowed)

    def list(self, request, companies_pk=None, installation_pk=None, gateway_pk=None, sensor_pk=None, format=None):
        queryset = self.queryset.filter(gateway_id=gateway_pk)
        serializer = SensorSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, companies_pk=None, installation_pk=None, gateway_pk=None, pk=None, format=None, *args, **kwargs):
        request.data['gateway'] = gateway_pk
        return super(SensorViewSet, self).create(request, *args, **kwargs)

    @detail_route(methods=['get'])
    def new_config(self, request, gateway_pk=None, pk=None):
        sensor = get_object_or_404(self.queryset, pk=pk)
        serializer = SensorSerializer(sensor)
        return Response(serializer.data,template_name='data/sensor_new_config.html')

    @detail_route(methods=['get'])
    def edit(self, request, gateway_pk, pk=None,format=None):
        sensor = get_object_or_404(self.queryset, pk=pk)
        serializer = SensorSerializer(sensor)
        return Response(serializer.data, status=status.HTTP_200_OK, template_name='data/sensor-edit.html')

    @detail_route(methods=['get'])
    def archive(self, request, gateway_pk, pk=None, format=None):
        sensor = get_object_or_404(self.queryset, pk=pk)
        serializer = SensorSerializer(sensor)
        return Response(serializer.data, status=status.HTTP_200_OK, template_name='data/sensor-archive.html')


class MeasurementViewSet(
                        mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet
                    ):
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
    permission_classes = (IsGatewayOrAuthenticated, IsUserAllowed,)

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

    @list_route(methods=['get'])
    def overview(self, request, gateway_pk=None, sensor_pk=None, format=None):
        """
        GET Request Filtering:
        /gateways/$1/sensors/$2/measurements?start=2015-01-01&end=2015-02-01&type=0
        Returns only measurement from sensor with ID $2 which have a timestamp that is in the range start -> end.
        type= measurement type
        """
        type = self.request.query_params.get('type', 0)
        step = int(self.request.query_params.get('step', 2))

        queryset = self.queryset.filter(sensor_id=sensor_pk)
        queryset = queryset.filter(measurement_type=type)

        extrapolatedData = queryset[::step] # get subsequent 2nd item

        serializer = MeasurementSerializer(extrapolatedData, many=True)
        return Response({'measurements': serializer.data})

    def retrieve(self, request, gateway_pk=None, sensor_pk=None, pk=None, format=None):
        queryset = get_object_or_404(self.queryset, sensor_id=sensor_pk, measurement_id=pk)
        self.check_object_permissions(self.request, queryset)
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

        serializer = MeasurementCreationSerializer(data=listOfThings, many=True)
        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response({'measurements': serializer.data},
                            status=status.HTTP_201_CREATED,
                            headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SensorConfigurationViewSet(HTMLGenericViewSet):
    """
    /gateways/$1/sensors/$2/config
    """
    queryset = SensorConfiguration.objects.all()
    serializer_class = SensorConfigurationSerializer

    def list(self, request, gateway_pk=None, sensor_pk=None, format=None):
        queryset = self.queryset.filter(sensor=sensor_pk)
        serializer = SensorConfigurationSerializer(queryset, many=True)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def edit(self, request, gateway_pk=None, sensor_pk=None, pk=None,format=None):
        sensorConf = get_object_or_404(self.queryset, pk=pk)
        serializer = SensorConfigurationSerializer(sensorConf)

        return Response(serializer.data, status=status.HTTP_200_OK, template_name='data/sensorconfiguration-detail.html')

    def destroy(self, request, gateway_pk, format=None, *args, **kwargs):
        result = super(SensorConfigurationViewSet, self).destroy(request, *args, **kwargs)

        if format == None or format == 'html':
            response = HttpResponse(content="", status=303)
            response["Location"] = reverse('gateway-detail', args=gateway_pk)
            return response
        else:
            return result

    # Redirect example
    # @detail_route(methods=['get'])
    # def test(self, request, gateway_pk, *args, **kwargs):
    #     response = HttpResponse(content="", status=303)
    #     response["Location"] = reverse('gateway-detail', args=gateway_pk)
    #     return response

class MeasurementTypeViewSet(HTMLGenericViewSet):
    """
    /measurement-type
    """
    queryset=MeasurementType.objects.all()
    serializer_class = MeasurementTypeSerializer

    @list_route(methods=['get'])
    def new(self, request):
        return Response()


class AlertViewSet(HTMLGenericViewSet):
    queryset=Alert.objects.all()
    serializer_class = AlertSerializer

    @detail_route(methods=['get'])
    def alert(self, request, pk=None, format=None):
        alert = get_object_or_404(self.queryset, pk=pk)
        serializer = AlertSerializer(alert)
        return Response(serializer.data, template_name='data/alert-detail.html')

    @detail_route(methods=['get'])
    def archive(self, request, gateway_pk=None, sensor_pk=None, pk=None, format=None):
        alert = get_object_or_404(self.queryset, pk=pk)
        alert.archived = True
        alert.save()
        return redirect('company-list')


class UserViewSet(HTMLGenericViewSet):
    queryset = User.objects.all()

    def list(self, request):
        return Response(template_name='data/profile.html')
