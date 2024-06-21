from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('heat/', views.HeatCalculationViewSet.as_view({'post':'create'}), name='heat calculation'),
    path('signup/', views.register, name='signup'),
    path('login/', views.userauth, name='login'),
]
