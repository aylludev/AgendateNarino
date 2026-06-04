from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from .models import Message
from usuarios.models import Usuario


@login_required
def inbox(request):
    """Inbox split-view: lista de conversaciones (izq) + preview/chat (der)."""
    from django.db.models import Max

    sent = Message.objects.filter(remitente=request.user).values_list('destinatario_id', flat=True)
    received = Message.objects.filter(destinatario=request.user).values_list('remitente_id', flat=True)
    peer_ids = list(set(list(sent) + list(received)))

    conversations = []
    for pid in peer_ids:
        last_msg = Message.objects.filter(
            Q(remitente=request.user, destinatario_id=pid) |
            Q(destinatario=request.user, remitente_id=pid)
        ).order_by('-created_at').first()

        unread = Message.objects.filter(
            remitente_id=pid, destinatario=request.user, leido=False
        ).count()

        if last_msg:
            peer = last_msg.destinatario if last_msg.remitente == request.user else last_msg.remitente
            conversations.append({
                'pk': peer.pk,
                'nombres': peer.nombres,
                'apellidos': peer.apellidos,
                'last_message': last_msg.descripcion,
                'last_message_date': last_msg.created_at,
                'unread': unread,
            })

    conversations.sort(key=lambda x: x['last_message_date'], reverse=True)

    # Conversación seleccionada (preview panel)
    selected_peer = None
    messages = []
    room_name = None
    peer_id = request.GET.get('with')
    if peer_id:
        try:
            selected_peer = Usuario.objects.get(pk=peer_id)
        except (Usuario.DoesNotExist, ValueError):
            selected_peer = None

    if selected_peer and selected_peer != request.user:
        ids = sorted([request.user.id, selected_peer.id])
        room_name = f"chat_{ids[0]}_{ids[1]}"

        messages = Message.objects.filter(
            Q(remitente=request.user, destinatario=selected_peer) |
            Q(remitente=selected_peer, destinatario=request.user)
        ).order_by('created_at')

        # Marcar como leídos los mensajes recibidos
        Message.objects.filter(
            remitente=selected_peer, destinatario=request.user, leido=False
        ).update(leido=True)

    return render(request, 'messaging/inbox.html', {
        'conversations': conversations,
        'selected_peer': selected_peer,
        'messages': messages,
        'room_name': room_name,
    })


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
            msg = Message.objects.create(
                remitente=remitente,
                destinatario=destinatario,
                descripcion=descripcion
            )
            messages.success(request, 'Mensaje enviado correctamente.')
            return redirect('messaging:chat_room', user_id=destinatario.pk)
        except Usuario.DoesNotExist:
            messages.error(request, 'Destinatario no encontrado.')

    from usuarios.models import Usuario
    usuarios = Usuario.objects.filter(is_active=True).exclude(pk=request.user.pk)
    return render(request, 'messaging/compose.html', {'usuarios': usuarios})


@login_required
def chat_room(request, user_id):
    """Render chat room with a specific user."""
    peer = get_object_or_404(Usuario, pk=user_id)
    if peer == request.user:
        return redirect('messaging:inbox')

    # Get or create room name
    ids = sorted([request.user.id, peer.id])
    room_name = f"chat_{ids[0]}_{ids[1]}"

    # Conversations: users we've exchanged messages with
    sent = Message.objects.filter(remitente=request.user).values_list('destinatario_id', flat=True)
    received = Message.objects.filter(destinatario=request.user).values_list('remitente_id', flat=True)
    peer_ids = list(set(list(sent) + list(received)))

    conversations = []
    for pid in peer_ids:
        last_msg = Message.objects.filter(
            Q(remitente=request.user, destinatario_id=pid) |
            Q(destinatario=request.user, remitente_id=pid)
        ).order_by('-created_at').first()
        if last_msg:
            peer_conv = last_msg.destinatario if last_msg.remitente == request.user else last_msg.remitente
            if peer_conv.pk != request.user.pk:
                conversations.append({
                    'pk': peer_conv.pk,
                    'nombres': peer_conv.nombres,
                    'apellidos': peer_conv.apellidos,
                    'last_message': last_msg.descripcion,
                    'last_message_date': last_msg.created_at,
                })

    conversations.sort(key=lambda x: x['last_message_date'], reverse=True)

    # All messages between these two users
    messages_qs = Message.objects.filter(
        Q(remitente=request.user, destinatario=peer) |
        Q(remitente=peer, destinatario=request.user)
    ).order_by('created_at')

    return render(request, 'messaging/chat.html', {
        'peer': peer,
        'room_name': room_name,
        'conversations': conversations,
        'messages': messages_qs,
    })
