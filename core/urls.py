from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cliente/', views.client_dashboard, name='client_dashboard'),
]