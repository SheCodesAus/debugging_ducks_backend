from django.urls import path, include
from . import views

urlpatterns = [
    path('lists/', views.IndividualLists.as_view()),
    path('lists/<int:pk>/', views.IndividualLists.as_view(), name='individual-list-detail'),

]