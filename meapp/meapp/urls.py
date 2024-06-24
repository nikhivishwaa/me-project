from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/calculation/', include('calculate.urls'), name='calculation'),
    path('dashboard/', include('home.urls'), name='dashboard'),
    path('', include('accounts.urls'), name='home'),
    path('', views.landingpage, name='landingpage'),
]
