from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from data_analysis.models import Company

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
        print(id)

        url = "/rest/companies/{}/".format(id) #Trailing slash needed, else redirect HTTP Code 301.
        data = {"name": "Duck Industries"}
        print(url)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Company.objects.get(pk=id).name, 'Duck Industries')



