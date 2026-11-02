from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect


class RolRequeridoMixin(LoginRequiredMixin, PermissionRequiredMixin):
    """Exige sesión iniciada y el permiso indicado en `permission_required`.

    - Sin sesión: redirige al login.
    - Con sesión pero sin permiso (ej. Asistente intentando crear): mensaje y
      redirección al inicio.
    """

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, "No tienes permisos para realizar esta acción.")
            return redirect("inicio")
        return super().handle_no_permission()
