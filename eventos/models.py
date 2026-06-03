from django.db import models
from usuarios.models import Usuario


class Categoria(models.Model):
    """Categoría para clasificar eventos."""

    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nombre'
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción'
    )
    activo = models.BooleanField(
        default=True,
        verbose_name='¿Activo?'
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
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Evento(models.Model):
    """Evento cultural con toda la información de ubicación y horario."""

    ESTADO_CHOICES = [
        ('no_iniciado', 'No Iniciado'),
        ('en_curso', 'En Curso'),
        ('finalizado', 'Finalizado'),
    ]
    TIPO_CHOICES = [
        ('abierto', 'Abierto al Público'),
        ('control_entradas', 'Control de Entradas'),
    ]

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='eventos',
        verbose_name='Categoría'
    )
    gestor = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name='gestionados',
        verbose_name='Gestor Cultural',
        null=True,
        blank=True,
    )
    titulo = models.CharField(
        max_length=200,
        verbose_name='Título'
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción'
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='no_iniciado',
        verbose_name='Estado'
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        verbose_name='Tipo'
    )
    link_formulario = models.URLField(
        blank=True,
        verbose_name='Link Formulario de Inscripción'
    )
    municipio = models.CharField(
        max_length=100,
        verbose_name='Municipio'
    )
    direccion = models.CharField(
        max_length=255,
        verbose_name='Dirección'
    )
    ubicacion = models.CharField(
        max_length=255,
        verbose_name='Ubicación'
    )
    detalles_ubicacion = models.TextField(
        blank=True,
        verbose_name='Detalles de Ubicación'
    )
    horario = models.TimeField(
        verbose_name='Horario'
    )
    geolocalizacion = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Geolocalización (lat,lng)'
    )
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Precio'
    )
    fecha = models.DateField(
        verbose_name='Fecha'
    )
    activo = models.BooleanField(
        default=True,
        verbose_name='¿Activo?'
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
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['-fecha']

    def __str__(self):
        return self.titulo


class EventoFlyer(models.Model):
    """Archivo multimedia (imagen/video) asociado a un evento."""

    TIPO_CHOICES = [
        ('imagen', 'Imagen'),
        ('video', 'Video'),
    ]

    evento = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE,
        related_name='flyers',
        verbose_name='Evento'
    )
    archivo = models.FileField(
        upload_to='eventos/flyers/',
        verbose_name='Archivo'
    )
    tipo = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES,
        default='imagen',
        verbose_name='Tipo'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )

    class Meta:
        verbose_name = 'Flyer de Evento'
        verbose_name_plural = 'Flyers de Eventos'

    def __str__(self):
        return f"Flyer {self.tipo} - {self.evento.titulo}"
