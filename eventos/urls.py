from django.urls import path
from . import views

app_name = 'eventos'

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.EventoListView.as_view(), name='evento_list'),
    path('events/add/', views.EventoCreateView.as_view(), name='evento_create'),
    path('events/<int:pk>/', views.EventoDetailView.as_view(), name='evento_detail'),
    path('events/<int:pk>/edit/', views.EventoUpdateView.as_view(), name='evento_update'),
    path('events/<int:pk>/delete/', views.EventoDeleteView.as_view(), name='evento_delete'),
    path('categories/', views.categoria_list, name='categoria_list'),
    path('categories/add/', views.CategoriaCreateView.as_view(), name='categoria_create'),
    path('categories/<int:pk>/edit/', views.CategoriaUpdateView.as_view(), name='categoria_update'),
    path('categories/<int:pk>/delete/', views.CategoriaDeleteView.as_view(), name='categoria_delete'),
]
