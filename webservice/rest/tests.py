from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from data_analysis.models import *

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
            "ip_address" : "192.168.1.2",
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
