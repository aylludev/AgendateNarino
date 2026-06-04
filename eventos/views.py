from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Categoria, Evento, EventoFlyer
from .forms import CategoriaForm, EventoForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView


def home(request):
    """Landing page pública (templates/home/index.html)."""
    return render(request, 'home/index.html')


def _is_moderador(user):
    return user.is_admin_or_mod()


@method_decorator(login_required, name='dispatch')
class EventoListView(ListView):
    model = Evento
    template_name = 'eventos/evento_list.html'
    context_object_name = 'eventos'
    paginate_by = 10

    def get_queryset(self):
        queryset = Evento.objects.select_related('categoria', 'gestor').order_by('-fecha')
        if not self.request.user.is_admin_or_mod():
            queryset = queryset.filter(gestor=self.request.user)
        buscar = self.request.GET.get('buscar')
        if buscar:
            queryset = queryset.filter(titulo__icontains=buscar)
        estado = self.request.GET.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Events'
        base_qs = Evento.objects.all()
        if not self.request.user.is_admin_or_mod():
            base_qs = base_qs.filter(gestor=self.request.user)
        context['total_count'] = base_qs.count()
        context['categorias'] = Categoria.objects.filter(activo=True)
        context['content_breadcrumbs'] = [{'label': 'Eventos', 'url': '', 'active': True}]
        return context


@method_decorator(login_required, name='dispatch')
class EventoCreateView(CreateView):
    model = Evento
    form_class = EventoForm
    template_name = 'eventos/evento_form.html'
    success_url = reverse_lazy('eventos:evento_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Crear Evento'
        ctx['content_breadcrumbs'] = [
            {'label': 'Events', 'url': reverse_lazy('eventos:evento_list'), 'active': False},
            {'label': 'Create', 'url': '', 'active': True},
        ]
        ctx['gestor_disabled'] = not _is_moderador(self.request.user)
        return ctx

    def get_initial(self):
        initial = super().get_initial()
        initial['gestor'] = self.request.user
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not _is_moderador(self.request.user):
            form.fields['gestor'].disabled = True
        return form

    def form_valid(self, form):
        if not form.instance.pk:
            form.instance.gestor = self.request.user
        messages.success(self.request, 'Evento creado exitosamente.')
        response = super().form_valid(form)
        self._save_flyer(form.instance)
        return response

    def _save_flyer(self, evento):
        flyer_file = self.request.FILES.get('flyer')
        if flyer_file:
            EventoFlyer.objects.create(
                evento=evento,
                archivo=flyer_file,
                tipo='imagen'
            )

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor corregí los errores.')
        return super().form_invalid(form)


@method_decorator(login_required, name='dispatch')
class EventoUpdateView(UpdateView):
    model = Evento
    form_class = EventoForm
    template_name = 'eventos/evento_form.html'
    success_url = reverse_lazy('eventos:evento_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Editar Evento'
        ctx['content_breadcrumbs'] = [
            {'label': 'Events', 'url': reverse_lazy('eventos:evento_list'), 'active': False},
            {'label': 'Edit', 'url': '', 'active': True},
        ]
        evento = self.get_object()
        user = self.request.user

        if _is_moderador(user):
            ctx['can_edit_estado'] = True
        elif evento.gestor == user and evento.estado == 'no_iniciado':
            ctx['can_edit_estado'] = True
        else:
            ctx['can_edit_estado'] = False

        return ctx

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        evento = self.get_object()
        is_mod = _is_moderador(user)
        is_owner = evento.gestor == user

        if is_mod:
            pass
        elif is_owner and evento.estado == 'no_iniciado':
            form.fields['gestor'].disabled = True
            form.fields.pop('estado', None)
            form.fields.pop('activo', None)
        else:
            for field in form.fields:
                form.fields[field].disabled = True

        return form

    def form_valid(self, form):
        messages.success(self.request, 'Evento actualizado exitosamente.')
        response = super().form_valid(form)
        self._save_flyer(form.instance)
        return response

    def _save_flyer(self, evento):
        flyer_file = self.request.FILES.get('flyer')
        if flyer_file:
            EventoFlyer.objects.create(
                evento=evento,
                archivo=flyer_file,
                tipo='imagen'
            )

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor corregí los errores.')
        return super().form_invalid(form)


@method_decorator(login_required, name='dispatch')
class EventoDeleteView(DeleteView):
    model = Evento
    template_name = 'eventos/evento_confirm_delete.html'
    success_url = reverse_lazy('eventos:evento_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Eliminar Evento'
        ctx['content_breadcrumbs'] = [
            {'label': 'Events', 'url': reverse_lazy('eventos:evento_list'), 'active': False},
            {'label': 'Delete', 'url': '', 'active': True},
        ]
        return ctx

    def delete(self, request, *args, **kwargs):
        evento = self.get_object()
        user = request.user
        is_mod = _is_moderador(user)
        is_owner = evento.gestor == user

        if is_mod or is_owner:
            evento.activo = False
            evento.save(update_fields=['activo'])
            messages.success(request, 'Evento desactivado.')
            return redirect(self.success_url)

        messages.error(request, 'No tienes permiso para eliminar este evento.')
        return redirect('eventos:evento_list')


@method_decorator(login_required, name='dispatch')
class EventoDetailView(DetailView):
    model = Evento
    template_name = 'eventos/evento_detail.html'
    context_object_name = 'evento'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = self.object.titulo
        ctx['content_breadcrumbs'] = [
            {'label': 'Events', 'url': reverse_lazy('eventos:evento_list'), 'active': False},
            {'label': 'Detail', 'url': '', 'active': True},
        ]
        return ctx


@method_decorator(login_required, name='dispatch')
class CategoriaCreateView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'eventos/categoria_form.html'
    success_url = reverse_lazy('eventos:categoria_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Crear Categoría'
        ctx['content_breadcrumbs'] = [
            {'label': 'Categorías', 'url': reverse_lazy('eventos:categoria_list'), 'active': False},
            {'label': 'Crear', 'url': '', 'active': True},
        ]
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Categoría creada exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor corregí los errores.')
        return super().form_invalid(form)


@method_decorator(login_required, name='dispatch')
class CategoriaUpdateView(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'eventos/categoria_form.html'
    success_url = reverse_lazy('eventos:categoria_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Editar Categoría'
        ctx['content_breadcrumbs'] = [
            {'label': 'Categorías', 'url': reverse_lazy('eventos:categoria_list'), 'active': False},
            {'label': 'Editar', 'url': '', 'active': True},
        ]
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Categoría actualizada.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor corregí los errores.')
        return super().form_invalid(form)


@method_decorator(login_required, name='dispatch')
class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = 'eventos/categoria_confirm_delete.html'
    success_url = reverse_lazy('eventos:categoria_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Eliminar Categoría'
        ctx['content_breadcrumbs'] = [
            {'label': 'Categorías', 'url': reverse_lazy('eventos:categoria_list'), 'active': False},
            {'label': 'Eliminar', 'url': '', 'active': True},
        ]
        return ctx

    def delete(self, request, *args, **kwargs):
        categoria = self.get_object()
        if categoria.eventos.exists():
            messages.error(request, 'No se puede eliminar la categoría porque tiene eventos asociados.')
            return redirect('eventos:categoria_list')
        messages.success(request, 'Categoría eliminada.')
        return super().delete(request, *args, **kwargs)


@login_required
def categoria_list(request):
    categorias = Categoria.objects.filter(activo=True).order_by('nombre')
    return render(request, 'eventos/categoria_list.html', {
        'categorias': categorias,
        'title': 'Categorías',
        'content_breadcrumbs': [{'label': 'Categorías', 'url': '', 'active': True}]
    })
