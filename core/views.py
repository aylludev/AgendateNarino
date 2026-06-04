from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q
from datetime import date, timedelta
from django.utils import timezone
from django.db.models.functions import TruncMonth
import json

from eventos.models import Evento
from messaging.models import Message


@login_required
def dashboard(request):
    """Dashboard para Admin y Moderador con métricas completas."""

    # Métricas básicas
    total_eventos = Evento.objects.count()
    eventos_activos = Evento.objects.filter(activo=True).count()
    total_gestores = Evento.objects.values('gestor').distinct().count()
    mensajes_nuevos = Message.objects.filter(destinatario=request.user, leido=False).count()

    # Estados de eventos
    eventos_no_iniciados = Evento.objects.filter(estado='no_iniciado').count()
    eventos_en_curso = Evento.objects.filter(estado='en_curso').count()
    eventos_finalizados = Evento.objects.filter(estado='finalizado').count()

    total = total_eventos if total_eventos > 0 else 1
    eventos_no_iniciados_pct = int(eventos_no_iniciados / total * 100)
    eventos_en_curso_pct = int(eventos_en_curso / total * 100)
    eventos_finalizados_pct = int(eventos_finalizados / total * 100)

    # Eventos este mes
    today = date.today()
    first_day_month = today.replace(day=1)
    eventos_mes = Evento.objects.filter(fecha__gte=first_day_month).count()

    # Ingresos estimados
    ingresos_estimados = Evento.objects.filter(activo=True).aggregate(
        total=Sum('precio'))['total'] or 0

    # Eventos por mes (últimos 6 meses)
    six_months_ago = today - timedelta(days=180)
    eventos_por_mes_data = (Evento.objects
        .filter(fecha__gte=six_months_ago)
        .annotate(month=TruncMonth('fecha'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month'))

    eventos_por_mes = [e['count'] for e in eventos_por_mes_data]

    meses_labels = [e['month'].strftime('%Y-%m-%d') for e in eventos_por_mes_data]

    # Rellenar con ceros si hay meses sin eventos
    if len(eventos_por_mes) < 6:
        default_labels = []
        default_data = []
        for i in range(5, -1, -1):
            d = today - timedelta(days=i*30)
            default_labels.append(d.strftime('%Y-%m-01'))
            default_data.append(0)
        # Mezclar con datos reales
        for i, l in enumerate(default_labels):
            for e in eventos_por_mes_data:
                if e['month'].strftime('%Y-%m') in l:
                    default_data[i] = e['count']
        eventos_por_mes = default_data
        meses_labels = default_labels

    # Úlitmos eventos
    ultimos_eventos = Evento.objects.select_related('categoria').order_by('-created_at')[:5]

    # Últimos mensajes
    ultimos_mensajes = Message.objects.filter(
        destinatario=request.user
    ).select_related('remitente').order_by('-created_at')[:5]

    return render(request, 'core/dashboard.html', {
        'total_eventos': total_eventos,
        'eventos_activos': eventos_activos,
        'total_gestores': total_gestores,
        'mensajes_nuevos': mensajes_nuevos,
        'eventos_no_iniciados': eventos_no_iniciados,
        'eventos_en_curso': eventos_en_curso,
        'eventos_finalizados': eventos_finalizados,
        'eventos_no_iniciados_pct': eventos_no_iniciados_pct,
        'eventos_en_curso_pct': eventos_en_curso_pct,
        'eventos_finalizados_pct': eventos_finalizados_pct,
        'eventos_mes': eventos_mes,
        'ingresos_estimados': ingresos_estimados,
        'eventos_por_mes': json.dumps(eventos_por_mes),
        'meses_labels': json.dumps(meses_labels),
        'ultimos_eventos': ultimos_eventos,
        'ultimos_mensajes': ultimos_mensajes,
    })


@login_required
def client_dashboard(request):
    """Dashboard para Gestor Cultural."""
    gestor = request.user
    mis_eventos = Evento.objects.filter(gestor=gestor).order_by('-fecha')
    mis_eventos_activos = mis_eventos.filter(activo=True, estado='no_iniciado').count()
    total_mis_eventos = mis_eventos.count()
    proximo = mis_eventos.filter(activo=True, fecha__gte=date.today()).first()
    proximo_evento = proximo.fecha.strftime('%d/%m') if proximo else '-'
    mensajes_nuevos = Message.objects.filter(destinatario=request.user, leido=False).count()

    return render(request, 'core/client_dashboard.html', {
        'mis_eventos': mis_eventos,
        'mis_eventos_activos': mis_eventos_activos,
        'total_mis_eventos': total_mis_eventos,
        'proximo_evento': proximo_evento,
        'mensajes_nuevos': mensajes_nuevos,
    })
