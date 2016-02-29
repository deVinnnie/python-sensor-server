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
        url = '/rest/companies/'
        data = {"name" : "ACME Industries", "installations":[]}
        response = self.client.post(url, data, format='json')
        self.company_id = response.data['company_id']

    def test_create_installation(self):
        """
        Ensure we can create a new installation object.
        """

        # Create a new installation within company
        url = '/rest/companies/{}/installations/'.format(self.company_id)
        data = {"name" : "Very Expensive ACME Installation", "gateways" : []}
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
        url = '/rest/companies/{}/installations/'.format(self.company_id)
        data = {"name" : "Very Expensive ACME Installation", "gateways" : []}
        response = self.client.post(url, data, format='json')
        installation_id = response.data['installation_id']

        url = '/rest/companies/{}/installations/{}/'.format(self.company_id, installation_id)
        data = {"name" : "Super Expensive ACME Installation"}

        response = self.client.patch(url, data, format='json')

        installation = Installation.objects.get(pk=installation_id)
        self.assertEqual(installation.name , 'Super Expensive ACME Installation')
        self.assertEqual(installation.company.company_id, self.company_id)
