from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from apps.organization.models import Organization
from apps.user.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class OrganizationAPITestCase(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            first_name='Orkhan', last_name='Anvarli', email='anvarliorxan10@gmail.com', password='Orxan1'
        )
        self.organization = Organization.objects.create(
            name='Remind',
            phone_number='994554708786',
            address='Mir Calal',
            owner=self.owner
        )

        self.client.force_authenticate(user=self.owner)


    def test_create_organization_with_owner(self):
        url = '/api/organization/create'
        data = {
                "name": "Remind",
                "phone_number": "994554708786",
                "address": "Mir Calal",
                "owner": {
                    "first_name": "Orkhan",
                    "last_name": "Anvarli",
                    "email": "anvarliorxan11@gmail.com",
                    "password": "Orxan1"
                }
            }

        response = self.client.post(url, data, format='json')
        self.assertEqual(201, response.status_code)



    def test_create_organization_member(self):
        url = '/api/organization/create-member'

        data = {
                "first_name": "Orkhan",
                "last_name": "Anvarli",
                "email": "anvarliorkhan1@gmail.com"
            }
        response = self.client.post(url, data, format='json')
        self.assertEqual(201, response.status_code)

