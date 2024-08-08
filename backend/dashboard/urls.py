from django.urls import path
from dashboard import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
]

