from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.register, name='signup'),
    path('login/', views.userauth, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('verifyemail/', views.verifyemail, name='verifyemail'),
]
