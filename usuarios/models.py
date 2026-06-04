from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver


class Usuario(AbstractUser):
    """Usuario personalizado que extiende AbstractUser con campos adicionales."""

    Cedula = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Cédula'
    )
    nombres = models.CharField(
        max_length=100,
        verbose_name='Nombres'
    )
    apellidos = models.CharField(
        max_length=100,
        verbose_name='Apellidos'
    )
    telefono = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Teléfono'
    )
    direccion = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Dirección'
    )
    is_moderador = models.BooleanField(
        default=False,
        verbose_name='¿Es moderador?'
    )
    created_by = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='created_usuarios',
        verbose_name='Creado por'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    updated_by = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='updated_usuarios',
        verbose_name='Última actualización por'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última actualización'
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.Cedula})"

    def in_group(self, group_name):
        """Check if user belongs to a group by name."""
        return self.groups.filter(name=group_name).exists()

    def is_gestor(self):
        """True si pertenece al grupo Gestor."""
        return self.in_group('Gestor')

    def is_moderador_miembro(self):
        """True si pertenece al grupo Moderador."""
        return self.in_group('Moderador')

    def is_admin_or_mod(self):
        """True si es staff, superuser o miembro del grupo Moderador."""
        return self.is_staff or self.is_superuser or self.in_group('Moderador')

    def save(self, *args, **kwargs):
        # Si ya tiene pk, sincronizar is_moderador con pertenencia al grupo
        # (no se puede consultar la M2M groups antes de tener pk).
        if self.pk is not None:
            if self.in_group('Moderador') and not self.is_moderador:
                self.is_moderador = True
            elif not self.in_group('Moderador') and self.is_moderador:
                self.is_moderador = False
        super().save(*args, **kwargs)


@receiver(m2m_changed, sender=Usuario.groups.through)
def sync_is_moderador(sender, instance, action, **kwargs):
    """Sincroniza is_moderador cuando cambia la membresía de grupos."""
    if action in ('post_add', 'post_remove', 'post_clear'):
        instance.is_moderador = instance.in_group('Moderador')
        # Avoid triggering signal again by updating without going through save()
        Usuario.objects.filter(pk=instance.pk).update(is_moderador=instance.is_moderador)

