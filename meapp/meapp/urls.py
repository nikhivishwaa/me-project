from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path('root/admin/', admin.site.urls),
    path('api/calculation/', include('calculate.urls'), name='calculation'),
    path('', include('home.urls'), name='dashboard'),
    path('', include('accounts.urls'), name='home'),
]
