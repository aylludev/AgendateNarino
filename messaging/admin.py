from django.contrib import admin
from .models import Message, Calification


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['remitente', 'destinatario', 'created_at']
    list_filter = ['remitente', 'destinatario', 'created_at']
    search_fields = ['remitente__username', 'remitente__nombres', 'destinatario__username', 'destinatario__nombres']
    readonly_fields = ['remitente', 'created_at']


@admin.register(Calification)
class CalificationAdmin(admin.ModelAdmin):
    list_display = ['gestor', 'evento', 'puntuacion', 'created_at']
    list_filter = ['puntuacion', 'evento', 'created_at']
    search_fields = ['gestor__nombres', 'gestor__apellidos', 'evento__titulo', 'comentario']
    readonly_fields = ['created_at', 'updated_at']
