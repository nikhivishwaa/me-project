from django.urls import path, include
from . import views

urlpatterns = [
        path('', views.dashboard, name='dashboard'),
        path('calculate/', views.calculate, name='calculate'),
]
