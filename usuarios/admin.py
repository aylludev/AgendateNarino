from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import Usuario


@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'Cedula', 'nombres', 'apellidos', 'is_moderador', 'is_active', '_groups']
    list_filter = ['is_active', 'is_staff', 'groups']
    search_fields = ['username', 'email', 'Cedula', 'nombres', 'apellidos']
    fieldsets = UserAdmin.fieldsets + (
        ('Datos personales', {'fields': ('Cedula', 'nombres', 'apellidos', 'telefono', 'direccion')}),
    )

    def _groups(self, obj):
        return ', '.join(g.name for g in obj.groups.all()) if obj.groups.exists() else '-'
    _groups.short_description = 'Grupos'

    filter_horizontal = ['groups', 'user_permissions']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change:
            # Recalculate is_moderador from group membership after save
            obj.is_moderador = obj.groups.filter(name='Moderador').exists()
            Usuario.objects.filter(pk=obj.pk).update(is_moderador=obj.is_moderador)
