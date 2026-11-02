from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import Categoria, Producto

User = get_user_model()


class BaseTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("setup_roles")
        cls.categoria = Categoria.objects.create(nombre="Redes")
        cls.producto = Producto.objects.create(
            sku="RE-001", nombre="Router", categoria=cls.categoria,
            precio=Decimal("50000"), stock=3, stock_minimo=5,
        )
        cls.admin = User.objects.create_user("admin1", password="Clave12345!")
        cls.admin.groups.add(Group.objects.get(name="Administrador"))
        cls.asistente = User.objects.create_user("asis1", password="Clave12345!")
        cls.asistente.groups.add(Group.objects.get(name="Asistente"))


class AccesoTests(BaseTest):
    def test_anonimo_es_redirigido_al_login(self):
        resp = self.client.get(reverse("producto_list"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse("login"), resp.url)

    def test_asistente_puede_ver_pero_no_crear(self):
        self.client.login(username="asis1", password="Clave12345!")
        self.assertEqual(self.client.get(reverse("producto_list")).status_code, 200)
        resp = self.client.get(reverse("producto_create"))
        self.assertEqual(resp.status_code, 302)

    def test_administrador_puede_crear(self):
        self.client.login(username="admin1", password="Clave12345!")
        resp = self.client.post(reverse("producto_create"), {
            "sku": "re-002", "nombre": "Switch", "categoria": self.categoria.pk,
            "precio": "30000", "stock": 10, "stock_minimo": 4, "activo": "on",
        })
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Producto.objects.filter(sku="RE-002").exists())


class ReporteTests(BaseTest):
    def test_reporte_calcula_valor_total(self):
        self.client.login(username="asis1", password="Clave12345!")
        resp = self.client.get(reverse("reporte"))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["resumen"]["valor_total"], Decimal("150000"))
        self.assertEqual(len(resp.context["stock_critico"]), 1)
