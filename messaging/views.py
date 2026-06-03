from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import Message


@login_required
def inbox(request):
    messages_list = Message.objects.filter(destinatario=request.user).order_by('-created_at')
    paginator = Paginator(messages_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'messaging/inbox.html', {'page_obj': page_obj})


@login_required
def sent(request):
    messages_list = Message.objects.filter(remitente=request.user).order_by('-created_at')
    paginator = Paginator(messages_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'messaging/sent.html', {'page_obj': page_obj})


@login_required
def delete_message(request, pk):
    """Delete a message. Only sender or moderator (group) can delete."""
    message = get_object_or_404(Message, pk=pk)

    user = request.user
    if user == message.remitente or user.is_moderador_miembro():
        message.delete()
        messages.success(request, 'Mensaje eliminado.')
    else:
        messages.error(request, 'No tienes permiso para eliminar este mensaje.')

    return redirect(request.META.get('HTTP_REFERER', reverse('messaging:inbox')))


@login_required
def compose(request):
    if request.method == 'POST':
        remitente = request.user
        destinatario_id = request.POST.get('destinatario')
        descripcion = request.POST.get('descripcion')

        from usuarios.models import Usuario
        try:
            destinatario = Usuario.objects.get(pk=destinatario_id)
            Message.objects.create(
                remitente=remitente,
                destinatario=destinatario,
                descripcion=descripcion
            )
            messages.success(request, 'Mensaje enviado correctamente.')
            return redirect('messaging:inbox')
        except Usuario.DoesNotExist:
            messages.error(request, 'Destinatario no encontrado.')

    from usuarios.models import Usuario
    usuarios = Usuario.objects.filter(is_active=True).exclude(pk=request.user.pk)
    return render(request, 'messaging/compose.html', {'usuarios': usuarios})
