from django.urls import path
from .views import ProjectView, RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # path('',),
    path('projects/', ProjectView.as_view(), name='projects-api'),

    path('user/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/signup/', RegisterView.as_view(), name='user_signup')
]
