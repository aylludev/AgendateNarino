import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Message

Usuario = get_user_model()


def get_room_name(user_id_1, user_id_2):
    """Room name ordered to ensure same room regardless of who initiates."""
    ids = sorted([int(user_id_1), int(user_id_2)])
    return f"chat_{ids[0]}_{ids[1]}"


class ChatConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for 1:1 chat."""

    async def connect(self):
        self.me = self.scope['url_route']['kwargs']['user_id']
        self.room_name = get_room_name(self.me, self.scope['user'].id)

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

        # Send last messages on connect
        messages = await self.get_last_messages()
        await self.send(text_data=json.dumps({
            'type': 'history',
            'messages': messages,
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        text = data.get('message', '').strip()
        if not text:
            return

        destinatario_id = data.get('destinatario_id')
        msg = await self.save_message(destinatario_id, text)

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'message': msg['message'],
                'sender_id': msg['sender_id'],
                'sender_nombre': msg['sender_nombre'],
                'destinatario_id': msg['destinatario_id'],
                'created_at': msg['created_at'],
                'message_id': msg['message_id'],
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'sender_id': event['sender_id'],
            'sender_nombre': event['sender_nombre'],
            'destinatario_id': event['destinatario_id'],
            'created_at': event['created_at'],
            'message_id': event['message_id'],
        }))

    @database_sync_to_async
    def get_last_messages(self):
        ids = sorted([self.me, self.scope['user'].id])
        room = f"chat_{ids[0]}_{ids[1]}"
        msgs = Message.objects.filter(
            room_identifier=room
        ).order_by('created_at')[:50]
        return [self.serialize_message(m) for m in msgs]

    @database_sync_to_async
    def save_message(self, destinatario_id, text):
        remitente = self.scope['user']
        destinatario = Usuario.objects.get(pk=destinatario_id)
        ids = sorted([remitente.id, destinatario.id])
        room = f"chat_{ids[0]}_{ids[1]}"

        msg = Message.objects.create(
            remitente=remitente,
            destinatario=destinatario,
            descripcion=text,
            room_identifier=room,
        )
        return self.serialize_message(msg)

    def serialize_message(self, msg):
        return {
            'message_id': msg.id,
            'message': msg.descripcion,
            'sender_id': msg.remitente_id,
            'sender_nombre': f"{msg.remitente.nombres} {msg.remitente.apellidos}",
            'destinatario_id': msg.destinatario_id,
            'created_at': msg.created_at.isoformat(),
        }