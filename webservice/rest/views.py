from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from data_analysis.models import *
from rest.serializers import *
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework import views

@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'gateways': reverse('gateway-list', request=request, format=format),
        'sensors': reverse('sensor-list', request=request, format=format)
    })


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
        app = 'rest'
        name = meta.object_name.lower()

        templates = {
            'list': ["%s/%s-list.html" % (app, name), "list.html"],
            'retrieve': ["%s/%s-detail.html" % (app, name), "detail.html"],

            'add': ["%s/%s-create.html" % (app, name), "create.html"],
            'edit': ["%s/%s-update.html" % (app, name), "update.html"],
            'delete': ["%s/%s-destroy.html" % (app, name), "destroy.html"],
        }

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


class InstallationViewSet(viewsets.ModelViewSet, HTMLGenericViewSet):
    """
    /installations
    """
    renderer_classes = HTMLGenericViewSet.renderer_classes
    queryset = Installation.objects.all()
    serializer_class = InstallationSerializer

    def list(self, request, companies_pk=None, format=None):
        queryset = self.queryset.filter(company_id=companies_pk)

        serializer = InstallationSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, companies_pk=None, pk=None, format=None):
        queryset = get_object_or_404(self.queryset, installation_id=pk)
        serializer = InstallationSerializer(queryset)
        return Response(serializer.data)

    def create(self, request, companies_pk=None, pk=None, format=None, *args, **kwargs):
        request.data['company'] = companies_pk
        return super(InstallationViewSet, self).create(request, *args, **kwargs)


class GatewayViewSet(viewsets.ModelViewSet, HTMLGenericViewSet):
    """
    /gateways
    """
    renderer_classes = HTMLGenericViewSet.renderer_classes
    queryset = Gateway.objects.all()
    serializer_class = GatewaySerializer

    def list(self, request, companies_pk=None, installation_pk=None, gateway_pk=None, format=None):
        queryset = self.queryset.filter(installation_id=installation_pk)
        if installation_pk == None:
            queryset = self.queryset
        serializer = GatewaySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, companies_pk=None, installation_pk=None, pk=None, format=None):
        queryset = get_object_or_404(self.queryset, gateway_id=pk)
        serializer = GatewaySerializer(queryset)
        return Response(serializer.data)

    def create(self, request, companies_pk=None, installation_pk=None, pk=None, format=None, *args, **kwargs):
        request.data['installation'] = installation_pk
        return super(GatewayViewSet, self).create(request, *args, **kwargs)


class GatewayConfigurationViewSet(viewsets.ModelViewSet):
    """
    /gateways/$1/config
    """
    renderer_classes = HTMLGenericViewSet.renderer_classes
    queryset = GatewayConfiguration.objects.all()
    serializer_class = GatewayConfigurationSerializer

    def list(self, request, companies_pk=None, installation_pk=None, gateway_pk=None, format=None):
        queryset = self.queryset.filter(gateway=gateway_pk)
        serializer = GatewayConfigurationSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, companies_pk=None, installation_pk=None, gateway_pk=None, pk=None, format=None):
        queryset = get_object_or_404(self.queryset, gateway_id=pk)
        serializer = GatewayConfigurationSerializer(queryset)
        return Response(serializer.data)

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


class MeasurementViewSet(viewsets.ModelViewSet, HTMLGenericViewSet):
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
    renderer_classes = HTMLGenericViewSet.renderer_classes


    def list(self, request, companies_pk=None, installation_pk=None, gateway_pk=None, sensor_pk=None, format=None):
        queryset = self.queryset.filter(sensor_id=sensor_pk)
        serializer = MeasurementSerializer(queryset, many=True)
        return Response( {'measurements': serializer.data}) #, template_name = 'measurements.html')

    def retrieve(self, request, companies_pk=None, installation_pk=None, gateway_pk=None, sensor_pk=None, pk=None, format=None):
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


class SensorConfigurationViewSet(viewsets.ModelViewSet):
    """
    /gateways/$1/sensors/$2/config
    """
    queryset = SensorConfiguration.objects.all()
    serializer_class = SensorConfigurationSerializer

    def list(self, request, companies_pk=None, installation_pk=None, gateway_pk=None, sensor_pk=None, format=None):
        queryset = self.queryset.filter(sensor=sensor_pk)
        serializer = GatewayConfigurationSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, companies_pk=None, installation_pk=None, gateway_pk=None, pk=None, format=None):
        queryset = get_object_or_404(self.queryset, gateway_id=pk)
        serializer = GatewayConfigurationSerializer(queryset)
        return Response(serializer.data)


#
# class GatewayList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Gateway.objects.all()
#     serializer_class = GatewaySerializer
# 
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
# 
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#         

# class GatewayDetail(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Gateway.objects.all()
#     serializer_class = GatewaySerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class SensorList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Sensor.objects.all()
#     serializer_class = SensorSerializer
# 
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
# 
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
# 
# 
# class SensorDetail(APIView):
#     """
#     Retrieve, update or delete a snippet instance.
#     """
#     def get_object(self, pk):
#         try:
#             return Sensor.objects.get(pk=pk)
#         except Sensor.DoesNotExist:
#             raise Http404
# 
#     def get(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SensorSerializer(snippet)
#         return Response(serializer.data)
# 
#     def put(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SensorSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# 
#     def delete(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
