from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from apps.organization.models import Organization
from apps.user.models import User
from apps.task.models import Task
from datetime import datetime, timedelta


class TaskAPITestCase(APITestCase):
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


        self.assignee = User.objects.create_user(
            first_name='Member', last_name='User', email='memberuser@gmail.com', password='Member1'
        )

        self.client.force_authenticate(user=self.owner)

    def test_create_task(self):
        url = '/api/task/create'

        data = {
            "title": "Make User System",
            "description": "Make user system for eTaskify",
            "deadline": "2024-11-10",
            "assigned_users": [self.assignee.id]
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(201, response.status_code)

    def test_get_tasks(self):
        url = f'/api/tasks'

        response = self.client.get(url, format='json')
        self.assertEqual(200, response.status_code)
