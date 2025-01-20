from django.urls import path, include
from . import views

urlpatterns = [
    path('lists/', views.IndividualLists.as_view()),
    path('lists/<int:pk>/', views.IndividualLists.as_view(), name='individual-list-detail'),
    path('listcategory/<int:pk>/', views.CategoryList.as_view(), name='list-category-detail'),
]