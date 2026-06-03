from django.contrib import admin
from django.db.models import ProtectedError
from django.utils.html import format_html
from .models import Categoria, Evento, EventoFlyer


class EventoFlyerInline(admin.TabularInline):
    model = EventoFlyer
    extra = 1
    readonly_fields = ['created_at']


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo', 'created_at']
    list_filter = ['activo', 'created_at']
    search_fields = ['nombre']
    readonly_fields = ['created_at', 'updated_at']

    def delete_model(self, request, obj):
        if obj.eventos.exists():
            self.message_user(request, f'No se puede eliminar la categoría "{obj.nombre}" porque tiene eventos asociados.', level='error')
            return
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.eventos.exists():
                self.message_user(request, f'No se puede eliminar la categoría "{obj.nombre}" porque tiene eventos asociados.', level='error')
                return
        super().delete_queryset(request, queryset)


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'categoria', 'gestor', 'estado', 'tipo', 'fecha', 'precio', 'activo']
    list_filter = ['estado', 'tipo', 'activo', 'categoria', 'created_at']
    search_fields = ['titulo', 'municipio', 'categoria__nombre', 'gestor__nombres', 'gestor__apellidos']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [EventoFlyerInline]

    fieldsets = (
        ('Información General', {
            'fields': ('categoria', 'gestor', 'titulo', 'descripcion')
        }),
        ('Estado y Tipo', {
            'fields': ('estado', 'tipo', 'link_formulario', 'activo')
        }),
        ('Ubicación', {
            'fields': ('municipio', 'direccion', 'ubicacion', 'detalles_ubicacion', 'geolocalizacion')
        }),
        ('Horario y Precio', {
            'fields': ('horario', 'fecha', 'precio')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(EventoFlyer)
class EventoFlyerAdmin(admin.ModelAdmin):
    list_display = ['evento', 'tipo', 'archivo', 'created_at']
    list_filter = ['tipo', 'created_at']
    search_fields = ['evento__titulo']
    readonly_fields = ['created_at']
