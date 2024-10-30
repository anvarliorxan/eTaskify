from django.urls import path
from api.organization import CreateOrganizationAPI
from api.organization import CreateMemberApi
from api.user import UserLoginApi
from api.task import CreateTaskAPI
from api.task import ListTaskAPI

urlpatterns = [
    # Organization
    path('organization/create',  CreateOrganizationAPI.as_view()),
    path('organization/create-member', CreateMemberApi.as_view()),

    # Task
    path('tasks',  ListTaskAPI.as_view()),
    path('task/create',  CreateTaskAPI.as_view()),

    # User
    path('user/login',  UserLoginApi.as_view()),
]
