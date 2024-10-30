from rest_framework import serializers
from apps.user.models import User


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters long.")

        if not any(char.isalnum() for char in value):
            raise serializers.ValidationError("Password must contain at least one alphanumeric character.")

        return value

    def create(self, validated_data):
        if User.objects.filter(email=validated_data["email"]).exists():
            raise serializers.ValidationError("This email already exists!")

        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user



class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',]
