from django.test import TestCase
from django.db import IntegrityError
from usuarios.models import Usuario
from .models import Categoria, Evento, EventoFlyer


class CategoriaModelTest(TestCase):
    """Test cases for Categoria model."""

    def setUp(self):
        self.categoria = Categoria.objects.create(
            nombre='Teatro',
            descripcion='Eventos de teatro y obras escénicas',
            activo=True
        )

    def test_categoria_creation(self):
        """Test that a Categoria can be created."""
        self.assertEqual(self.categoria.nombre, 'Teatro')
        self.assertTrue(self.categoria.activo)

    def test_categoria_str(self):
        """Test the string representation of Categoria."""
        self.assertEqual(str(self.categoria), 'Teatro')

    def test_categoria_unique_nombre(self):
        """Test that Categoria nombre must be unique."""
        with self.assertRaises(IntegrityError):
            Categoria.objects.create(nombre='Teatro')

    def test_categoria_default_activo(self):
        """Test that activo defaults to True."""
        categoria = Categoria.objects.create(nombre='Música')
        self.assertTrue(categoria.activo)


class EventoModelTest(TestCase):
    """Test cases for Evento model."""

    def setUp(self):
        self.usuario = Usuario.objects.create(
            username='1094912345',
            Cedula='1094912345',
            nombres='Carlos',
            apellidos='González',
            email='carlos@example.com'
        )
        self.categoria = Categoria.objects.create(nombre='Teatro')
        self.evento = Evento.objects.create(
            categoria=self.categoria,
            gestor=self.usuario,
            titulo='Obra de Teatro Regional',
            descripcion='Una obra de teatro tradicional de Nariño',
            estado='no_iniciado',
            tipo='abierto',
            municipio='Pasto',
            direccion='Calle 5 #3-45',
            ubicacion='Teatro Municipal',
            horario='19:00',
            fecha='2026-06-15',
            precio=0,
            activo=True
        )

    def test_evento_creation(self):
        """Test that an Evento can be created with all fields."""
        self.assertEqual(self.evento.titulo, 'Obra de Teatro Regional')
        self.assertEqual(self.evento.estado, 'no_iniciado')
        self.assertEqual(self.evento.tipo, 'abierto')
        self.assertTrue(self.evento.activo)

    def test_evento_estado_choices(self):
        """Test that Evento estado choices are enforced."""
        self.assertIn(self.evento.estado, ['no_iniciado', 'en_curso', 'finalizado'])

    def test_evento_tipo_choices(self):
        """Test that Evento tipo choices are enforced."""
        self.assertIn(self.evento.tipo, ['abierto', 'control_entradas'])

    def test_evento_str(self):
        """Test the string representation of Evento."""
        self.assertEqual(str(self.evento), 'Obra de Teatro Regional')

    def test_evento_fk_to_categoria(self):
        """Test that Evento has FK to Categoria."""
        self.assertEqual(self.evento.categoria.nombre, 'Teatro')

    def test_evento_fk_to_gestor(self):
        """Test that Evento has FK to gestor."""
        self.assertEqual(self.evento.gestor.nombres, 'Carlos')

    def test_evento_default_estado(self):
        """Test that Evento default estado is no_iniciado."""
        evento = Evento.objects.create(
            categoria=self.categoria,
            gestor=self.usuario,
            titulo='Otro Evento',
            tipo='abierto',
            municipio='Pasto',
            direccion='Calle 10',
            ubicacion='Centro',
            horario='20:00',
            fecha='2026-07-01'
        )
        self.assertEqual(evento.estado, 'no_iniciado')


class EventoFlyerModelTest(TestCase):
    """Test cases for EventoFlyer model."""

    def setUp(self):
        self.usuario = Usuario.objects.create(
            username='1094912345',
            Cedula='1094912345',
            nombres='Carlos',
            apellidos='González',
            email='carlos@example.com'
        )
        self.categoria = Categoria.objects.create(nombre='Teatro')
        self.evento = Evento.objects.create(
            categoria=self.categoria,
            gestor=self.usuario,
            titulo='Obra de Teatro Regional',
            tipo='abierto',
            municipio='Pasto',
            direccion='Calle 5 #3-45',
            ubicacion='Teatro Municipal',
            horario='19:00',
            fecha='2026-06-15'
        )
        self.flyer = EventoFlyer.objects.create(
            evento=self.evento,
            tipo='imagen'
        )

    def test_eventoflyer_creation(self):
        """Test that an EventoFlyer can be created."""
        self.assertEqual(self.flyer.evento, self.evento)
        self.assertEqual(self.flyer.tipo, 'imagen')

    def test_eventoflyer_default_tipo(self):
        """Test that EventoFlyer default tipo is imagen."""
        self.assertEqual(self.flyer.tipo, 'imagen')

    def test_eventoflyer_str(self):
        """Test the string representation of EventoFlyer."""
        self.assertEqual(str(self.flyer), 'Flyer imagen - Obra de Teatro Regional')
