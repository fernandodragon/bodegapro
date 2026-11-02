from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

MODELOS = ("categoria", "producto")


class Command(BaseCommand):
    help = "Crea los grupos Administrador (CRUD completo) y Asistente (solo lectura)."

    def handle(self, *args, **options):
        admin_group, _ = Group.objects.get_or_create(name="Administrador")
        asistente_group, _ = Group.objects.get_or_create(name="Asistente")

        permisos_admin, permisos_asistente = [], []
        for modelo in MODELOS:
            for accion in ("add", "change", "delete", "view"):
                perm = Permission.objects.get(
                    content_type__app_label="inventario",
                    codename=f"{accion}_{modelo}",
                )
                permisos_admin.append(perm)
                if accion == "view":
                    permisos_asistente.append(perm)

        admin_group.permissions.set(permisos_admin)
        asistente_group.permissions.set(permisos_asistente)
        self.stdout.write(self.style.SUCCESS("Roles configurados: Administrador y Asistente."))
