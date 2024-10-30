from rest_framework import serializers
from .models import Task
from apps.user.serializers import ListUserSerializer
from apps.core.utils.sendgrid_email import sendgrid_send_email


class TaskListSerializer(serializers.ModelSerializer):
    assigned_users = ListUserSerializer(many=True, read_only=True)
    created_by = ListUserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'deadline', 'status', 'assigned_users',
            'created_by', 'created',
        ]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'deadline', 'assigned_users']

    def create(self, validated_data):
        assigned_users = validated_data.pop('assigned_users', None)
        task = Task.objects.create(**validated_data, created_by=self.context['request'].user,
                                   organization=self.context['request'].user.my_organization.first())

        if assigned_users:
            task.assigned_users.set(assigned_users)
            for user in assigned_users:
                sendgrid_send_email(to_email=user.email, subject="You have a new task")

        return task


