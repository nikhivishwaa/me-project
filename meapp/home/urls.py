from django.urls import path, include
from . import views

urlpatterns = [
        path('', views.landingpage, name='home'),
        path('dashboard/', views.dashboard, name='dashboard'),
        path('calculator/', views.calculate, name='calculator'),
        path('about/', views.about, name='about'),
        path('contact/', views.contact, name='contact'),
]
