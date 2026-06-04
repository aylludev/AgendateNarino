"""
Pobla la base de datos con datos de ejemplo realistas para Agendate Nariño.

Uso:
    python manage.py seed_data           # datos frescos
    python manage.py seed_data --clear   # borra todo antes de insertar
"""

from datetime import date, timedelta
from decimal import Decimal
from random import choice, randint

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction

from eventos.models import Categoria, Evento, EventoFlyer
from usuarios.models import Usuario


# ── Categorías ──────────────────────────────────────────────────────────

CATEGORIAS = [
    ("Música", "Conciertos, presentaciones musicales y festivales de sonido"),
    ("Danza", "Espectáculos de danza folclórica, contemporánea y tradicional"),
    ("Teatro", "Obras teatrales, monólogos y presentaciones escénicas"),
    ("Gastronomía", "Ferias gastronómicas, muestras culinarias y cocina tradicional"),
    ("Artesanías", "Exposiciones y ferias de artesanías nariñenses"),
    ("Cine y Audiovisuales", "Muestras de cine, documentales y producciones audiovisuales"),
    ("Festivales", "Festivales culturales integrales y eventos tradicionales"),
    ("Literatura", "Lecturas, lanzamientos de libros y encuentros literarios"),
    ("Deportes", "Eventos deportivos, torneos y actividades recreativas"),
    ("Patrimonio", "Ferias de patrimonio cultural, historia y museos"),
]

# ── Municipios de Nariño con coordenadas aproximadas ────────────────────

MUNICIPIOS = [
    ("Pasto", 1.2136, -77.2811),
    ("Tumaco", 1.8066, -78.7646),
    ("Ipiales", 0.8285, -77.6406),
    ("La Unión", 1.6032, -77.1315),
    ("Túquerres", 1.0924, -77.6181),
    ("Barbacoas", 1.6722, -78.1316),
    ("Samaniego", 1.3385, -77.5950),
    ("Sandona", 1.2895, -77.4694),
    ("El Charco", 2.4770, -78.1100),
    ("Cumbal", 0.9080, -77.7913),
]

# ── Gestores culturales ─────────────────────────────────────────────────

GESTORES = [
    {
        "username": "ana.arteaga",
        "nombres": "Ana",
        "apellidos": "Arteaga Rosero",
        "Cedula": "1234567890",
        "email": "ana.arteaga@agendatenarino.co",
        "telefono": "3001234567",
        "direccion": "Cra 25 # 18-30, Pasto",
    },
    {
        "username": "luis.coral",
        "nombres": "Luis Carlos",
        "apellidos": "Coral Burbano",
        "Cedula": "2345678901",
        "email": "luis.coral@agendatenarino.co",
        "telefono": "3012345678",
        "direccion": "Calle 10 # 5-20, La Unión",
    },
    {
        "username": "maria.quintana",
        "nombres": "María Fernanda",
        "apellidos": "Quintana",
        "Cedula": "3456789012",
        "email": "maria.quintana@agendatenarino.co",
        "telefono": "3023456789",
        "direccion": "Av. Los Libertadores # 15-45, Ipiales",
    },
    {
        "username": "jorge.tenorio",
        "nombres": "Jorge Eduardo",
        "apellidos": "Tenorio Castillo",
        "Cedula": "4567890123",
        "email": "jorge.tenorio@agendatenarino.co",
        "telefono": "3034567890",
        "direccion": "Calle del Comercio # 8-12, Tumaco",
    },
    {
        "username": "diana.ceron",
        "nombres": "Diana Patricia",
        "apellidos": "Cerón Benavides",
        "Cedula": "5678901234",
        "email": "diana.ceron@agendatenarino.co",
        "telefono": "3045678901",
        "direccion": "Cra 3 # 10-25, Túquerres",
    },
    {
        "username": "hernan.vasquez",
        "nombres": "Hernán",
        "apellidos": "Vásquez Martínez",
        "Cedula": "6789012345",
        "email": "hernan.vasquez@agendatenarino.co",
        "telefono": "3056789012",
        "direccion": "Calle Real # 5-10, Samaniego",
    },
    {
        "username": "carmen.ordonez",
        "nombres": "Carmen Elena",
        "apellidos": "Ordoñez Guerra",
        "Cedula": "7890123456",
        "email": "carmen.ordonez@agendatenarino.co",
        "telefono": "3067890123",
        "direccion": "Cra 5 # 12-34, Barbacoas",
    },
    {
        "username": "pablo.articultura",
        "nombres": "Pablo Andrés",
        "apellidos": "Rosero Arteaga",
        "Cedula": "8901234567",
        "email": "pablo.rosero@agendatenarino.co",
        "telefono": "3078901234",
        "direccion": "Calle 18 # 20-30, Sandoná",
    },
]

# ── Eventos de ejemplo ──────────────────────────────────────────────────

EVENTOS_TEMPLATES = [
    {
        "titulo": "Festival Internacional de Música Andina",
        "descripcion": "Tres días de música tradicional andina con agrupaciones de Colombia, Ecuador y Perú. Incluye conciertos al aire libre, talleres de instrumentos autóctonos y una feria gastronómica.",
        "categoria": "Música",
        "municipio_idx": 0,  # Pasto
        "tipo": "abierto",
        "precio": 0,
        "dias_desde_hoy": 7,
    },
    {
        "titulo": "Feria Gastronómica 'Sabores de Nariño'",
        "descripcion": "Degustación de platos típicos nariñenses: cuy asado, empanadas de añejo, helado de paila, y más. Participan cocineros tradicionales de 15 municipios.",
        "categoria": "Gastronomía",
        "municipio_idx": 0,  # Pasto
        "tipo": "abierto",
        "precio": 10000,
        "dias_desde_hoy": 15,
    },
    {
        "titulo": "Muestra Departamental de Danza Folclórica",
        "descripcion": "Agrupaciones de danza de todo el departamento presentan coreografías tradicionales: bambuco, torbellino, currulao y danzas afrocolombianas.",
        "categoria": "Danza",
        "municipio_idx": 1,  # Tumaco
        "tipo": "abierto",
        "precio": 5000,
        "dias_desde_hoy": 10,
    },
    {
        "titulo": "Obra de Teatro: 'Relatos del Pacifico'",
        "descripcion": "Puesta en escena que narra historias y leyendas de la costa pacífica nariñense. Una fusión de teatro, música y danza.",
        "categoria": "Teatro",
        "municipio_idx": 1,  # Tumaco
        "tipo": "control_entradas",
        "precio": 15000,
        "dias_desde_hoy": 20,
    },
    {
        "titulo": "Expo-Artesanías Ipiales 2026",
        "descripcion": "Exposición y venta de artesanías de la frontera: tejidos en lana de borrego, cerámica decorada, y sombreros de paja toquilla.",
        "categoria": "Artesanías",
        "municipio_idx": 2,  # Ipiales
        "tipo": "abierto",
        "precio": 0,
        "dias_desde_hoy": 25,
    },
    {
        "titulo": "Festival del Cur uro y la Ollada",
        "descripcion": "Celebración tradicional del municipio de La Unión con muestras gastronómicas, danzas, comparsas y la tradicional ollada comunitaria.",
        "categoria": "Festivales",
        "municipio_idx": 3,  # La Unión
        "tipo": "abierto",
        "precio": 0,
        "dias_desde_hoy": 45,
    },
    {
        "titulo": "Taller de Literatura Infantil",
        "descripcion": "Taller gratuito para niños y jóvenes sobre escritura creativa y cuentos tradicionales nariñenses. Impartido por escritores locales.",
        "categoria": "Literatura",
        "municipio_idx": 4,  # Túquerres
        "tipo": "control_entradas",
        "precio": 0,
        "dias_desde_hoy": 8,
    },
    {
        "titulo": "Concierto de Música del Pacífico",
        "descripcion": "Agrupaciones de marimba de chonta y música tradicional del Pacífico colombiano se presentan en el Coliseo Municipal de Tumaco.",
        "categoria": "Música",
        "municipio_idx": 1,  # Tumaco
        "tipo": "control_entradas",
        "precio": 20000,
        "dias_desde_hoy": 30,
    },
    {
        "titulo": "Ciclo de Cine: 'Nariño en Pantalla'",
        "descripcion": "Proyección de documentales y cortometrajes realizados por cineastas nariñenses. Incluye conversatorio con los directores.",
        "categoria": "Cine y Audiovisuales",
        "municipio_idx": 0,  # Pasto
        "tipo": "abierto",
        "precio": 0,
        "dias_desde_hoy": 12,
    },
    {
        "titulo": "Feria de la Ciencia y la Cultura",
        "descripcion": "Exposición interactiva de proyectos científicos y culturales de instituciones educativas del departamento. Actividades para toda la familia.",
        "categoria": "Festivales",
        "municipio_idx": 5,  # Samaniego
        "tipo": "abierto",
        "precio": 0,
        "dias_desde_hoy": 60,
    },
    {
        "titulo": "Encuentro de Bandas Musicales Juveniles",
        "descripcion": "Bandas de viento y percusión de 10 municipios se reúnen en concierto. Formación musical y convivencia cultural.",
        "categoria": "Música",
        "municipio_idx": 7,  # Sandoná
        "tipo": "abierto",
        "precio": 0,
        "dias_desde_hoy": 35,
    },
    {
        "titulo": "Festival de la Cerveza Artesanal Nariñense",
        "descripcion": "Degustación de cervezas artesanales producidas en Nariño, con música en vivo, food trucks y shows culturales.",
        "categoria": "Gastronomía",
        "municipio_idx": 0,  # Pasto
        "tipo": "control_entradas",
        "precio": 25000,
        "dias_desde_hoy": 75,
    },
    {
        "titulo": "Exposición de Orquídeas y Flores del Sur",
        "descripcion": "Muestra de orquídeas nativas de Nariño y la región andina. Talleres de cultivo y jardinería.",
        "categoria": "Patrimonio",
        "municipio_idx": 8,  # El Charco
        "tipo": "abierto",
        "precio": 0,
        "dias_desde_hoy": 50,
    },
    {
        "titulo": "Torneo de Tejo y Deportes Autóctonos",
        "descripcion": "Competencia de tejo, rana y otros deportes tradicionales colombianos. Categorías amateur y profesional.",
        "categoria": "Deportes",
        "municipio_idx": 4,  # Túquerres
        "tipo": "control_entradas",
        "precio": 5000,
        "dias_desde_hoy": 18,
    },
    {
        "titulo": "Festival Afrocolombiano del Pacífico",
        "descripcion": "Celebración de la cultura afro con música, danza, gastronomía y ceremonias tradicionales del Pacífico nariñense.",
        "categoria": "Festivales",
        "municipio_idx": 1,  # Tumaco
        "tipo": "abierto",
        "precio": 10000,
        "dias_desde_hoy": 90,
    },
]


class Command(BaseCommand):
    help = "Pobla la base de datos con datos de ejemplo realistas para Agendate Nariño"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Elimina todos los eventos, categorías, y gestores antes de insertar",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self._clear_data()

        with transaction.atomic():
            self._create_groups()
            self._create_categorias()
            gestores = self._create_gestores()
            self._create_eventos(gestores)

        self.stdout.write(self.style.SUCCESS("✅ Base de datos poblada exitosamente"))

    def _clear_data(self):
        self.stdout.write("🧹 Limpiando datos existentes...")
        EventoFlyer.objects.all().delete()
        Evento.objects.all().delete()
        Categoria.objects.all().delete()
        Usuario.objects.exclude(is_superuser=True).delete()
        self.stdout.write(self.style.WARNING("   Eliminados eventos, categorías y usuarios no-superuser."))

    def _create_groups(self):
        for name in ("Gestor", "Moderador"):
            Group.objects.get_or_create(name=name)
        self.stdout.write("   Grupos: ✅")

    def _create_categorias(self):
        for nombre, descripcion in CATEGORIAS:
            Categoria.objects.get_or_create(nombre=nombre, defaults={"descripcion": descripcion})
        self.stdout.write(f"   Categorías: ✅ ({len(CATEGORIAS)} creadas)")

    def _create_gestores(self):
        grupo = Group.objects.get(name="Gestor")
        creados = []
        for data in GESTORES:
            usuario, created = Usuario.objects.get_or_create(
                username=data["username"],
                defaults={
                    "nombres": data["nombres"],
                    "apellidos": data["apellidos"],
                    "Cedula": data["Cedula"],
                    "email": data["email"],
                    "telefono": data["telefono"],
                    "direccion": data["direccion"],
                    "is_active": True,
                },
            )
            if created:
                usuario.set_password("gestor123")
                usuario.save()
                usuario.groups.add(grupo)
            creados.append(usuario)
        self.stdout.write(f"   Gestores: ✅ ({len(creados)} disponibles)")
        return creados

    def _create_eventos(self, gestores):
        cat_map = {c.nombre: c for c in Categoria.objects.all()}
        creados = 0
        for tmpl in EVENTOS_TEMPLATES:
            municipio, lat, lng = MUNICIPIOS[tmpl["municipio_idx"]]
            fecha = date.today() + timedelta(days=tmpl["dias_desde_hoy"])
            gestor = choice(gestores)

            evento, created = Evento.objects.get_or_create(
                titulo=tmpl["titulo"],
                defaults={
                    "categoria": cat_map[tmpl["categoria"]],
                    "gestor": gestor,
                    "descripcion": tmpl["descripcion"],
                    "estado": "no_iniciado",
                    "tipo": tmpl["tipo"],
                    "municipio": municipio,
                    "direccion": f"Calle {randint(1, 50)} # {randint(1, 20)}-{randint(1, 99)}",
                    "ubicacion": f"Centro de {municipio}",
                    "horario": f"{randint(8, 11):02d}:00:00",
                    "fecha": fecha,
                    "precio": tmpl["precio"],
                    "geolocalizacion": f"{lat:.4f},{lng:.4f}",
                    "activo": True,
                },
            )
            if created:
                creados += 1

        self.stdout.write(f"   Eventos: ✅ ({creados} nuevos, {Evento.objects.count()} total)")
