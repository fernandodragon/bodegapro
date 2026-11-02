from decimal import Decimal

from django.core.management.base import BaseCommand

from inventario.models import Categoria, Producto

DATOS = {
    "Notebooks": [
        ("NB-001", "Notebook 14\" i5 16GB", "649990", 12, 5),
        ("NB-002", "Notebook 15\" Ryzen 7", "789990", 6, 5),
        ("NB-003", "Notebook Gamer RTX", "1299990", 3, 4),
    ],
    "Periféricos": [
        ("PE-001", "Mouse inalámbrico", "12990", 60, 15),
        ("PE-002", "Teclado mecánico", "39990", 25, 10),
        ("PE-003", "Monitor 24\" Full HD", "119990", 4, 6),
        ("PE-004", "Webcam 1080p", "24990", 18, 8),
    ],
    "Redes": [
        ("RE-001", "Router WiFi 6", "59990", 14, 6),
        ("RE-002", "Switch 8 puertos", "29990", 20, 8),
        ("RE-003", "Cable UTP Cat6 (caja)", "89990", 2, 5),
    ],
    "Almacenamiento": [
        ("AL-001", "SSD NVMe 1TB", "69990", 30, 10),
        ("AL-002", "Disco externo 2TB", "74990", 9, 8),
        ("AL-003", "Pendrive 64GB", "7990", 80, 20),
    ],
}


class Command(BaseCommand):
    help = "Carga datos de ejemplo para la demostración (no duplica si ya existen)."

    def handle(self, *args, **options):
        creados = 0
        for nombre_cat, productos in DATOS.items():
            categoria, _ = Categoria.objects.get_or_create(nombre=nombre_cat)
            for sku, nombre, precio, stock, minimo in productos:
                _, nuevo = Producto.objects.get_or_create(
                    sku=sku,
                    defaults={
                        "nombre": nombre,
                        "categoria": categoria,
                        "precio": Decimal(precio),
                        "stock": stock,
                        "stock_minimo": minimo,
                    },
                )
                creados += int(nuevo)
        self.stdout.write(self.style.SUCCESS(f"Datos demo listos ({creados} productos nuevos)."))
