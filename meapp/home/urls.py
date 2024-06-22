from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.register, name='signup'),
    path('login/', views.userauth, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('api/calculation/', include('calculate.urls'), name='calculation'),
]
