from django import forms
from .models import Message, Calification


class MessageForm(forms.ModelForm):
    """Form for sending messages."""

    class Meta:
        model = Message
        fields = ['destinatario', 'descripcion']
        widgets = {
            'destinatario': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class CalificationForm(forms.ModelForm):
    """Form for califications."""

    class Meta:
        model = Calification
        fields = ['gestor', 'evento', 'puntuacion', 'comentario']
        widgets = {
            'gestor': forms.Select(attrs={'class': 'form-control'}),
            'evento': forms.Select(attrs={'class': 'form-control'}),
            'puntuacion': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_puntuacion(self):
        puntuacion = self.cleaned_data.get('puntuacion')
        if puntuacion < 1 or puntuacion > 5:
            raise forms.ValidationError('La puntuación debe estar entre 1 y 5.')
        return puntuacion
