from django.db import models
from apps.core.models import TimeStampedModel
from apps.user.models import User

class Organization(TimeStampedModel):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='my_organization')

    def __str__(self):
        return self.name
