from django.urls import path
from . import views
from users.views import CustomAuthToken

urlpatterns = [
    path("users/", views.CustomUserList.as_view()),
    path("users/<int:pk>/", views.CustomUserDetail.as_view()),
    path("api-token-auth/", CustomAuthToken.as_view(), name="api_token_auth"),
]
