from django.urls import path, include
from rest_framework import routers

from . import views

urlpatterns = [
    path('reports/', views.ReportsView.as_view(), name='reports'),
]