from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from apps.organization.models import Organization
from apps.user.models import User



class UserAPITestCase(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            first_name='Orkhan', last_name='Anvarli', email='anvarliorxan10@gmail.com', password='Orxan1'
        )

        self.organization = Organization.objects.create(
            name='Remind',
            phone_number='994554708786',
            address='Mir Calal',
            owner=self.owner,
        )
        self.organization.users.add(self.owner)

    def test_user_login(self):
        url = '/api/user/login'

        data = {
                "email": "anvarliorxan10@gmail.com",
                "password": "Orxan1"
               }

        response = self.client.post(url, data, format='json')
        self.assertEqual(200, response.status_code)

