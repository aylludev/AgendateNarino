from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView as AuthLoginView
from django_ratelimit.decorators import ratelimit
from .models import Usuario
from eventos.models import Evento
from .forms import UsuarioForm


@method_decorator(login_required, name='dispatch')
class UsuarioDetailView(DetailView):
    model = Usuario
    template_name = 'usuarios/usuario_detail.html'
    context_object_name = 'usuario'


@login_required
def usuario_list(request):
    if request.user.is_admin_or_mod() and request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        action = request.POST.get('action')
        usuario = get_object_or_404(Usuario, pk=usuario_id)

        if action == 'toggle_active':
            usuario.is_active = not usuario.is_active
            usuario.save(update_fields=['is_active'])
            estado = 'activado' if usuario.is_active else 'desactivado'
            messages.success(request, f'Usuario {estado} exitosamente.')
        elif action == 'toggle_mod':
            from django.contrib.auth.models import Group
            grupo_mod, _ = Group.objects.get_or_create(name='Moderador')
            if usuario.groups.filter(name='Moderador').exists():
                usuario.groups.remove(grupo_mod)
                messages.success(request, f'{usuario.nombres} ya no es moderador.')
            else:
                usuario.groups.add(grupo_mod)
                messages.success(request, f'{usuario.nombres} ahora es moderador.')

        return redirect('usuarios:usuario_list')

    usuarios = Usuario.objects.order_by('-date_joined')
    return render(request, 'usuarios/usuario_list.html', {'usuarios': usuarios})


@login_required
def usuario_detail(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    return render(request, 'usuarios/usuario_detail.html', {'usuario': usuario})


@login_required
def perfil(request):
    usuario = request.user
    eventos = Evento.objects.filter(gestor=usuario).order_by('-fecha')
    return render(request, 'usuarios/perfil.html', {
        'usuario': usuario,
        'eventos': eventos,
    })


class LoginView(AuthLoginView):
    template_name = 'usuarios/login.html'

    @method_decorator(ratelimit(key='post:username', rate='10/m', method='POST', block=True))
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        user = self.request.user
        if user.is_admin_or_mod():
            return '/core/dashboard/'
        elif user.is_gestor():
            return '/core/client_dashboard/'
        return '/'

    def form_invalid(self, form):
        messages.error(self.request, 'Usuario o contraseña inválidos')
        return super().form_invalid(form)


@ratelimit(key='post:username', rate='10/m', method='POST', block=True)
def registro(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            # Verificar términos aceptados
            if not request.POST.get('terms'):
                messages.error(request, 'Debés aceptar los términos y condiciones para registrarte.')
                return render(request, 'usuarios/registro.html', {'form': form})

            # Guardar el usuario (UsuarioForm.save() setea la contraseña)
            user = form.save()

            # Asignar grupo Gestor automáticamente
            from django.contrib.auth.models import Group
            grupo_gestor, _ = Group.objects.get_or_create(name='Gestor')
            user.groups.add(grupo_gestor)

            # Autenticar e iniciar sesión
            auth_user = authenticate(request, username=user.username, password=form.cleaned_data['password1'])
            if auth_user is not None:
                login(request, auth_user)
            messages.success(request, f'¡Cuenta creada! Bienvenido, {user.nombres}.')
            return redirect('core:client_dashboard')
        else:
            messages.error(request, 'Por favor corregí los errores indicados.')
            return render(request, 'usuarios/registro.html', {'form': form})
    return render(request, 'usuarios/registro.html')
