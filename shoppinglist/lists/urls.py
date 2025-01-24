from django.urls import path, include
from . import views

urlpatterns = [
    path("lists/", views.IndividualLists.as_view()),
    path("lists/<int:pk>/", views.ListDetail.as_view()),
    path("category/", views.ListCategory.as_view()),
    path("category/<int:pk>/", views.CategoryDetail.as_view()),
]
