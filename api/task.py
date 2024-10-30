from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.task.serializers import TaskSerializer
from apps.task.serializers import TaskListSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from apps.task.models import Task



class ListTaskAPI(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskListSerializer

    def get_queryset(self):
        return Task.objects.filter(organization=self.request.user.my_organization.first())


class CreateTaskAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = TaskSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            data = {
                "status": '200',
                "message": "Task created successfully",
                "result": serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)

        data = {
            "status": '400',
            "message": serializer.errors,
            "result": ''
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)