from rest_framework import serializers
from .models import Organization
from apps.user.serializers import UserSerializer


class OrganizationWithUserSerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Organization
        fields = ['name', 'phone_number', 'address', 'owner']

    def create(self, validated_data):
        owner_data = validated_data.pop('owner')

        owner = UserSerializer.create(UserSerializer(), validated_data=owner_data)
        organization = Organization.objects.create(**validated_data, owner=owner)
        organization.users.add(owner)
        return organization


class CreateMemberSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
