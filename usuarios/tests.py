from django.test import TestCase
from .models import Usuario


class UsuarioModelTest(TestCase):
    """Test cases for Usuario model."""

    def setUp(self):
        self.usuario = Usuario.objects.create(
            username='1094912345',
            Cedula='1094912345',
            nombres='Carlos',
            apellidos='González',
            email='carlos@example.com',
            telefono='3001234567',
            direccion='Calle 5 #3-45',
            is_moderador=False
        )

    def test_usuario_creation(self):
        """Test that a Usuario can be created with all fields."""
        self.assertEqual(self.usuario.username, '1094912345')
        self.assertEqual(self.usuario.Cedula, '1094912345')
        self.assertEqual(self.usuario.nombres, 'Carlos')
        self.assertEqual(self.usuario.apellidos, 'González')
        self.assertTrue(self.usuario.is_active)

    def test_usuario_str(self):
        """Test the string representation of Usuario."""
        expected = 'Carlos González (1094912345)'
        self.assertEqual(str(self.usuario), expected)

    def test_usuario_is_moderador_default_false(self):
        """Test that is_moderador defaults to False."""
        self.assertFalse(self.usuario.is_moderador)

    def test_usuario_timestamps(self):
        """Test that timestamps are auto-generated."""
        self.assertIsNotNone(self.usuario.created_at)
        self.assertIsNotNone(self.usuario.updated_at)
