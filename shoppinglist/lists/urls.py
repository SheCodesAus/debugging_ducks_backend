from django.urls import path, include
from . import views

urlpatterns = [
    path("items/", views.ItemsList.as_view()),
    path("items/<int:pk>/", views.ItemDetail.as_view()),
    path("items/bulk-update/", views.ItemBulkUpdate.as_view()),
    path("lists/", views.IndividualLists.as_view()),
    path("lists/<int:pk>/", views.ListDetail.as_view()),
    path("lists/user/", views.ListsFromLoggedInUser.as_view()),
    path("category/", views.IndividualCategory.as_view()),
    path("category/<int:pk>/", views.CategoryDetail.as_view()),
    path("category/user/", views.CategoriesFromLoggedInUser.as_view()),
]
