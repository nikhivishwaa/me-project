from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.register, name='signup'),
    path('login/', views.userauth, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('api/profile/', views.profile, name='profile'),
    path('verifyemail/', views.verifyemail, name='verifyemail'),
    path('forgotpassword/', views.forgotpasswordotp, name='forgotpassword'),
    path('newpassword/', views.newpassword, name='newpassword'),
]
