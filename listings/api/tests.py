""" Tests for the HouseViewSet """
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from api.models import HouseModel, SupportedStates
from django.contrib.auth.models import User


class HouseAPITests(APITestCase):
    """ API Test Class """
    def setUp(self):
        """ Pre Test Setup"""
        self.user = User.objects.create_user(username='anton', password='admin')
        self.house_1 = HouseModel.objects.create(
            address="123 Test St",
            city="San Francisco",
            state=SupportedStates.CA,
            zipcode="94117",
            home_size=1500,
            home_type="SingleFamily",
            area_unit="SqFt",
            price=1000000,
            tax_year=2023,
            zillow_id=12345678
        )
        self.house_2 = HouseModel.objects.create(
            address="124 Test St",
            city="Oakland",
            state=SupportedStates.CA,
            zipcode="94233",
            home_size=1500,
            home_type="SingleFamily",
            area_unit="SqFt",
            price=1000000,
            tax_year=2023,
            zillow_id=87654321
        )

    def test_house_list(self):
        """ Test list returns 2 houses """
        url = reverse('house-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        expected_uuids = sorted([str(self.house_1.uuid), str(self.house_2.uuid)])
        returned_uuids = sorted([house['uuid'] for house in response.data['results']])
        self.assertEqual(expected_uuids, returned_uuids)

    def test_house_detail(self):
        """ Test detail of the house on the serialzier """
        url = reverse('house-detail', kwargs={'uuid': self.house_1.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['state'], 'Lovely California')

    def test_reserve_house_success(self):
        """ Test auth user can reserve a house that was not reserved previously """
        self.client.login(username='anton', password='admin')
        self.assertFalse(self.house_1.reserved)
        url = reverse('house-reserve-house', kwargs={'uuid': self.house_1.uuid})
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.house_1.refresh_from_db()
        self.assertTrue(self.house_1.reserved)

    def test_reserve_house_fail_auth(self):
        """ Test user can not reserve a house without auth """
        self.assertFalse(self.house_1.reserved)
        url = reverse('house-reserve-house', kwargs={'uuid': self.house_1.uuid})
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.house_1.refresh_from_db()
        self.assertFalse(self.house_1.reserved)
