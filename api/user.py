from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from apps.user.serializers import UserLoginSerializer






class UserLoginApi(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")

            user = authenticate(request, email=email, password=password)

            if user:
                refresh = RefreshToken.for_user(user)
                result = {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user_id": user.id
                }
                data = {
                    "status": "200",
                    "message": "Account verified",
                    "result": result
                }
                return Response(data, status=status.HTTP_200_OK)

        response = {
            "status": "404",
            "message": "Invalid email or password",
            "results": serializer.errors
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)