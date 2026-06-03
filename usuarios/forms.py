from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

Usuario = get_user_model()


class UsuarioForm(forms.ModelForm):
    """Formulario de registro para Usuario."""

    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control rounded-4',
            'autocomplete': 'new-password',
            'aria-describedby': 'passwordHelp',
        }),
        help_text='''
            <small id="passwordHelp" class="form-text text-muted">
                Mínimo 8 caracteres, al menos una letra y un número.
            </small>
        ''',
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control rounded-4', 'autocomplete': 'new-password'}),
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'Cedula', 'nombres', 'apellidos', 'telefono', 'direccion']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control rounded-4'}),
            'email': forms.EmailInput(attrs={'class': 'form-control rounded-4'}),
            'Cedula': forms.TextInput(attrs={'class': 'form-control rounded-4', 'placeholder': 'Ej: 1085XXXXXX'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control rounded-4'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control rounded-4'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control rounded-4', 'placeholder': '300 XXX XXXX'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control rounded-4'}),
        }

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        if Usuario.objects.filter(username=username).exists():
            raise ValidationError('El nombre de usuario ya está registrado.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError('El correo electrónico ya está registrado.')
        return email

    def clean_Cedula(self):
        cedula = self.cleaned_data['Cedula'].strip()
        if len(cedula) < 7:
            raise ValidationError('La cédula debe tener al menos 7 dígitos.')
        if not cedula.isdigit():
            raise ValidationError('La cédula solo debe contener números.')
        if Usuario.objects.filter(Cedula=cedula).exists():
            raise ValidationError('La cédula ya está registrada.')
        return cedula

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if password:
            validate_password(password)
        return password

    def clean(self):
        super().clean()
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise ValidationError('Las contraseñas no coinciden.')
        return self.cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data['password1'])
        if commit:
            usuario.save()
        return usuario
