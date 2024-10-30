from django.db import models
from apps.user.models import User
from apps.core.models import TimeStampedModel
from apps.organization.models import Organization

class Task(TimeStampedModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField(null=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_users = models.ManyToManyField(User, related_name='tasks')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')

    def __str__(self):
        return self.title