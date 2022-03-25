from django.urls import path
from .views import RegisterView, ProjectView, TaskView, PermissionView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # path('',),
    path('user/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/signup/', RegisterView.as_view(), name='user_signup_api'),
    path('user/project/permission/', PermissionView.as_view(), name='user_project_permission'),

    path('projects/', ProjectView.as_view(), name='projects_api'),

    path('projects/tasks/', TaskView.as_view(), name='projects_task_api')
]

