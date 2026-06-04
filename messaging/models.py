from django.db import models
from usuarios.models import Usuario
from eventos.models import Evento


class Message(models.Model):
    """Mensaje entre usuarios."""

    remitente = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name='mensajes_enviados',
        verbose_name='Remitente'
    )
    destinatario = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name='mensajes_recibidos',
        verbose_name='Destinatario'
    )
    descripcion = models.TextField(
        verbose_name='Mensaje'
    )
    room_identifier = models.CharField(
        max_length=50,
        db_index=True,
        blank=True,
        default='',
        verbose_name='Identificador de sala'
    )
    leido = models.BooleanField(
        default=False,
        verbose_name='¿Leído?'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de envío'
    )

    class Meta:
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'
        ordering = ['-created_at']

    def __str__(self):
        return f"De {self.remitente} para {self.destinatario}"


class Calification(models.Model):
    """Calificación de un evento por parte de un gestor."""

    gestor = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name='calificaciones',
        verbose_name='Gestor'
    )
    evento = models.ForeignKey(
        Evento,
        on_delete=models.PROTECT,
        related_name='calificaciones',
        verbose_name='Evento'
    )
    puntuacion = models.IntegerField(
        verbose_name='Puntuación (1-5)'
    )
    comentario = models.TextField(
        blank=True,
        verbose_name='Comentario'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última actualización'
    )

    class Meta:
        verbose_name = 'Calificación'
        verbose_name_plural = 'Calificaciones'
        constraints = [
            models.UniqueConstraint(
                fields=['gestor', 'evento'],
                name='unique_calification_per_gestor_evento'
            )
        ]

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.puntuacion and (self.puntuacion < 1 or self.puntuacion > 5):
            raise ValidationError({'puntuacion': 'La puntuación debe estar entre 1 y 5.'})

    def save(self, *args, **kwargs):
        if not self.room_identifier:
            ids = sorted([self.remitente_id, self.destinatario_id])
            self.room_identifier = f"chat_{ids[0]}_{ids[1]}"
        self.clean()
        super().save(*args, **kwargs)
