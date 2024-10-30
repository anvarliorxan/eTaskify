from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.organization.serializers import OrganizationWithUserSerializer
from rest_framework.permissions import IsAuthenticated
from apps.user.models import User
from apps.organization.models import Organization
from apps.organization.serializers import CreateMemberSerializer
import random
import string


class CreateOrganizationAPI(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OrganizationWithUserSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            data = {
                "status": '200',
                "message": "Organization and user created successfully",
                "result": serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)

        data = {
            "status": '400',
            "message": serializer.errors,
            "result": ''
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class CreateMemberApi(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = CreateMemberSerializer(data=request.data)
        if serializer.is_valid():
            first_name = serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']
            email = serializer.validated_data['email']

            if User.objects.filter(email=email).exists():
                return Response({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            organization = Organization.objects.filter(owner=request.user).first()

            if organization is None:
                return Response({'error': 'You are not owner.'}, status=status.HTTP_400_BAD_REQUEST)


            new_user = User.objects.create(email=email, first_name=first_name,
                                           last_name=last_name, is_active=True,
                                           user_type='member')

            characters = string.ascii_letters + string.digits + string.punctuation
            # Generate a password with the specified length
            password = ''.join(random.choice(characters) for i in range(10))

            new_user.set_password(password)
            new_user.save()

            organization.users.add(new_user)
            organization.save()

            data = {
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email,
                'password': password
            }

            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
