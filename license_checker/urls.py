from django.urls import path
from . import views

urlpatterns = [
    path('check_license/', views.check_license),
    path('is_up/', views.is_up)
]
