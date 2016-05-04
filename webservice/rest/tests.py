from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from data_analysis.models import *
import datetime
from decimal import *

# Ensure that a migrations file is present. The test will create a new database.
# Without the correct migrations the db tables won't be created.

class CompanyTest(APITestCase):
    def test_create_company(self):
        """
        Ensure we can create a new company object.
        """
        url = '/rest/companies/'
        data = {"name" : "ACME Industries", "installations":[]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(Company.objects.get().name, 'ACME Industries')

    def test_create_company_without_installations_specified_fails(self):
        """
        Ensure we can't create a new company object specifying only the company name.
        """
        url = '/rest/companies/'
        data = {"name" : "ACME Industries"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_company(self):
        """
        Ensure we can update the company name.
        """
        url = '/rest/companies/'
        data = {"name" : "ACME Industries", "installations":[]}
        response = self.client.post(url, data, format='json')
        id = response.data['company_id']

        url = "/rest/companies/{}/".format(id) #Trailing slash needed, else redirect HTTP Code 301.
        data = {"name": "Duck Industries"}

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Company.objects.get(pk=id).name, 'Duck Industries')


class InstallationTest(APITestCase):
    def setUp(self):
        # Create a dummy company for use in further tests.
        company = Company.objects.create(name="ACME Industries")
        company.save()
        self.company_id = company.company_id
        self.company = company

    def test_create_installation(self):
        """
        Ensure we can create a new installation object.
        """

        # Create a new installation within company
        url = '/rest/installations/'
        data = {
            "name" : "Very Expensive ACME Installation",
            "gateways" : [],
            "company" : self.company_id
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.get(pk=self.company_id).installations.count(), 1)

        installation = Company.objects.get(pk=self.company_id).installations.get()
        self.assertEqual(installation.name, 'Very Expensive ACME Installation')
        self.assertEqual(installation.company.company_id, self.company_id)

    def test_update_installation_name(self):
        """
        Ensure we can update the installation name.
        """
        # Create a new installation within company
        installation = self.company.installations.create(name="Very Expensive ACME Installation")
        installation_id = installation.installation_id

        url = '/rest/installations/{}/'.format(installation_id)
        data = {"name" : "Super Expensive ACME Installation"}
        response = self.client.patch(url, data, format='json')

        installation  = Installation.objects.get(pk=installation_id) # Refresh instance
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(installation.name , 'Super Expensive ACME Installation')
        self.assertEqual(installation.company.company_id, self.company_id)


class GatewayTest(APITestCase):
    def setUp(self):
        # Create a dummy company.
        self.company = Company.objects.create(name="ACME Industries")
        self.company.save()

        # Create a new installation within company
        self.installation = self.company.installations.create(name="Very Expensive ACME Installation")

    def test_get_non_existant_gateway_returns_404(self):
        id = 4 # ID of a non existant gateway
        url = 'rest/gateways/{}/'.format(id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_gateway(self):
        url = '/rest/gateways/'
        data = {
            "sensors" : [],
            "config" : [],
            "installation" : self.installation.installation_id
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Gateway.objects.count(), 1)
        installation = Installation.objects.get(pk=self.installation.installation_id)
        self.assertEqual(installation.gateways.count(), 1) # Make sure the gateway is a child of the Installation.

    def test_update_gateway_ip(self):
        gateway = self.installation.gateways.create(ip_address="192.168.1.2")

        url = '/rest/gateways/{}/'.format(gateway.gateway_id)
        data = { "ip_address": "192.168.1.3" }
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        gateway = Gateway.objects.get(pk=gateway.gateway_id)
        self.assertEqual(gateway.ip_address, '192.168.1.3')


class SensorTest(APITestCase):
    def setUp(self):
        # Create a dummy company.
        self.company = Company.objects.create(name="ACME Industries")
        self.company.save()

        # Create a new installation within the company.
        self.installation = self.company.installations.create(name="Very Expensive ACME Installation")

        # Create a new gateway within the installation.
        self.gateway = self.installation.gateways.create(ip_address='192.168.1.2')

    def test_create_sensor(self):
        """
        Posting to /gateways/$1/sensors/
        {
            "name": "Awesome Sensor Node",
            "measurements": [],
            "config": []
        }
        creates a new sensor node in gateway $1
        """
        url = '/rest/gateways/{}/sensors/'.format(self.gateway.gateway_id)
        data = {
            "name": "Awesome Sensor Node",
            "measurements": [],
            "config": []
        }
        response = self.client.post(url, data, format='json')

        gateway = Gateway.objects.get(pk=self.gateway.gateway_id)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sensor.objects.count(), 1)
        self.assertEqual(gateway.sensors.count(), 1)

    def test_update_sensor(self):
        sensor = self.gateway.sensors.create(name="Awesome Sensor Node")

        url = '/rest/gateways/{}/sensors/{}/'.format(self.gateway.gateway_id, sensor.sensor_id)
        data = {
            "name": "Super Awesome Sensor Node",
        }
        response = self.client.patch(url, data, format='json')

        sensor = Sensor.objects.get(pk=sensor.sensor_id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(sensor.name, 'Super Awesome Sensor Node')


class MeasurementTest(APITestCase):
    def setUp(self):
        # Create a dummy company.
        self.company = Company.objects.create(name="ACME Industries")
        self.company.save()

        # Create a new installation within the company.
        self.installation = self.company.installations.create(name="Very Expensive ACME Installation")

        # Create a new gateway within the installation.
        self.gateway = self.installation.gateways.create(ip_address='192.168.1.2')

        self.sensor1 = self.gateway.sensors.create(name="Sensor Node")
        self.sensor2 = self.gateway.sensors.create(name="Sensor Node")
        self.sensor3 = self.gateway.sensors.create(name="Sensor Node")

        MeasurementType.objects.create(measurementTypeID=1, unit="F", scalar=1, name="Awesome Measurement")

    def test_create_single_measurement(self):
        url = '/rest/gateways/{}/sensors/{}/measurements/'.format(self.gateway.gateway_id, self.sensor1.sensor_id)

        data = { "measurements" : [
                    {   "timestamp" : "2015-01-01T00:00:00",
                        "sensor_id" : self.sensor1.sensor_id,
                        "measurement_type" : 1,
                        "value" : 12.3
                    }
        ]}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Measurement.objects.count(), 1)
        self.assertEqual(Sensor.objects.get(pk=self.sensor1.sensor_id).measurements.count(), 1)

        m = Measurement.objects.get()
        self.assertEqual(m.timestamp, datetime.datetime(2015,1,1,0,0))
        self.assertEqual(m.measurement_type, MeasurementType.objects.get(pk=1))
        self.assertEqual(m.value, 12.3)

    def test_create_multiple_measurement(self):
        url = '/rest/gateways/{}/sensors/{}/measurements/'.format(self.gateway.gateway_id, self.sensor1.sensor_id)

        data = { "measurements" : [
                    {   "timestamp" : "2015-01-01T00:00:00",
                        "sensor_id" : self.sensor1.sensor_id,
                        "measurement_type" : 1,
                        "value" : 12.3
                    },
                    {   "timestamp" : "2015-01-01T01:00:00",
                        "sensor_id" : self.sensor1.sensor_id,
                        "measurement_type" : 1,
                        "value" : 12.5
                    },
                    {   "timestamp" : "2015-01-01T02:00:00",
                        "sensor_id" : self.sensor1.sensor_id,
                        "measurement_type" : 1,
                        "value" : 11.4
                    }
        ]}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Measurement.objects.count(), 3)

    def test_delete_measurement_gives_error(self):
        """
        Measurements can only be added, not deleted.
        """
        m = Measurement.objects.create(timestamp="2015-01-01T00:00:00",
                                    sensor_id=self.sensor1,
                                    measurement_type = MeasurementType.objects.get(pk=1),
                                    value = 12.3)
        url = '/rest/gateways/{}/sensors/{}/measurements/{}/'.format(self.gateway.gateway_id, self.sensor1.sensor_id, m.measurement_id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_range_selection_returns_correct_measurements(self):
        """
        Ensure that the start and end parameters in a GET request return only measurements within the range start date to end date.
        """
        Measurement.objects.create(
                                    timestamp="2015-01-01T00:00:00",
                                    sensor_id=self.sensor1,
                                    measurement_type = MeasurementType.objects.get(pk=1),
                                    value = 12.3)
        Measurement.objects.create(
                                    timestamp="2015-05-09T00:00:00",
                                    sensor_id=self.sensor1,
                                    measurement_type = MeasurementType.objects.get(pk=1),
                                    value = 12.3)
        Measurement.objects.create(
                                    timestamp="2016-02-04T00:00:00",
                                    sensor_id=self.sensor1,
                                    measurement_type = MeasurementType.objects.get(pk=1),
                                    value = 12.3)
        Measurement.objects.create(
                                    timestamp="2016-03-04T00:00:00",
                                    sensor_id=self.sensor1,
                                    measurement_type = MeasurementType.objects.get(pk=1),
                                    value = 12.3)

        base_url = '/rest/gateways/{}/sensors/{}/measurements.json'.format(self.gateway.gateway_id, self.sensor1.sensor_id)

        url = base_url + '?start=2015-02-01&end=2016-02-20'
        response = self.client.get(url)
        self.assertEqual(2, len(response.data['measurements'])) #Two measurements expected

        url = base_url + '?start=2015-01-01&end=2017-01-01'
        response = self.client.get(url)
        self.assertEqual(4, len(response.data['measurements'])) #Four measurements expected

        url = base_url + '?start=2015-01-02&end=2015-12-30'
        response = self.client.get(url)
        self.assertEqual(1, len(response.data['measurements']))