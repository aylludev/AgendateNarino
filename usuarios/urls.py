from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Auth
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    # CRUD
    path('', views.usuario_list, name='usuario_list'),
    path('<int:pk>/', views.usuario_detail, name='usuario_detail'),
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.perfil, name='perfil'),
]