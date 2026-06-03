from django import forms
from .models import Categoria, Evento, EventoFlyer


class CategoriaForm(forms.ModelForm):
    """Form for Categoria."""

    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class EventoForm(forms.ModelForm):
    """Form for Evento with inline flyer support."""

    flyer = forms.FileField(
        required=False,
        label='Flyer del evento',
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
            'help_text': 'Formato: JPG, PNG, WebP. Máximo 5MB.'
        })
    )

    class Meta:
        model = Evento
        fields = [
            'gestor', 'categoria', 'titulo', 'descripcion',
            'estado', 'tipo', 'link_formulario', 'municipio',
            'direccion', 'ubicacion', 'detalles_ubicacion', 'horario',
            'geolocalizacion', 'precio', 'fecha'
        ]
        labels = {
            'gestor': 'Gestor Cultural',
            'categoria': 'Categoría',
            'titulo': 'Título del evento',
            'descripcion': 'Descripción',
            'estado': 'Estado',
            'tipo': 'Tipo de evento',
            'link_formulario': 'Link de inscripción',
            'municipio': 'Municipio',
            'direccion': 'Dirección',
            'ubicacion': 'Lugar / Venue',
            'detalles_ubicacion': 'Detalles de ubicación',
            'horario': 'Horario',
            'geolocalizacion': 'Coordenadas (lat, lng)',
            'precio': 'Precio (COP)',
            'fecha': 'Fecha del evento',
        }
        widgets = {
            'gestor': forms.Select(attrs={'class': 'form-select'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'link_formulario': forms.URLInput(attrs={'class': 'form-control'}),
            'municipio': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'detalles_ubicacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'horario': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'geolocalizacion': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class EventoFlyerForm(forms.ModelForm):
    """Form for EventoFlyer."""

    class Meta:
        model = EventoFlyer
        fields = ['archivo', 'tipo']
        widgets = {
            'archivo': forms.FileInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
        }
