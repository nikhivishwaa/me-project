from django.urls import path
from . import views

urlpatterns = [
    # path('', views.HeatCalculationViewSet.as_view({'post':'create'}), name='heat calculation'),
    path('', views.HeatCalculation, name='heat calculation fn'),
]
