from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    descripcion = models.TextField(blank=True)
    creada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "categoría"
        verbose_name_plural = "categorías"

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    sku = models.CharField(
        "SKU",
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                r"^[A-Z0-9-]+$",
                "Usa solo letras mayúsculas, números y guiones.",
            )
        ],
    )
    nombre = models.CharField(max_length=120)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="productos",
    )
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    stock = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=5)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="productos_creados",
    )

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.sku} - {self.nombre}"

    def clean(self):
        # Validación a nivel de modelo (se ejecuta en formularios y admin)
        if self.nombre and len(self.nombre.strip()) < 3:
            raise ValidationError({"nombre": "El nombre debe tener al menos 3 caracteres."})
        if self.sku:
            self.sku = self.sku.strip().upper()

    @property
    def valor_inventario(self):
        return self.precio * self.stock

    @property
    def stock_critico(self):
        return self.stock <= self.stock_minimo
