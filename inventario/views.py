from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import Group
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Avg, Count, DecimalField, ExpressionWrapper, F, Q, Sum, Value
from django.db.models.deletion import ProtectedError
from django.db.models.functions import Coalesce
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import CategoriaForm, ProductoForm, RegistroForm
from .mixins import RolRequeridoMixin
from .models import Categoria, Producto

User = get_user_model()

VALOR = DecimalField(max_digits=14, decimal_places=2)


# --------------------------------------------------------------------------
# Páginas generales y registro
# --------------------------------------------------------------------------
class InicioView(TemplateView):
    template_name = "inventario/inicio.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["total_productos"] = Producto.objects.count()
        ctx["total_categorias"] = Categoria.objects.count()
        return ctx


class RegistroView(CreateView):
    form_class = RegistroForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("inicio")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("inicio")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        # Todo usuario nuevo parte como Asistente (solo lectura)
        grupo, _ = Group.objects.get_or_create(name="Asistente")
        self.object.groups.add(grupo)
        login(self.request, self.object)
        messages.success(self.request, "Cuenta creada. ¡Bienvenido!")
        return response


# --------------------------------------------------------------------------
# CRUD de Productos
# --------------------------------------------------------------------------
class ProductoListView(RolRequeridoMixin, ListView):
    model = Producto
    permission_required = "inventario.view_producto"
    paginate_by = 10

    def get_queryset(self):
        # select_related evita una consulta extra por cada fila (problema N+1)
        qs = Producto.objects.select_related("categoria")
        q = self.request.GET.get("q", "").strip()
        categoria = self.request.GET.get("categoria", "").strip()
        if q:
            qs = qs.filter(Q(nombre__icontains=q) | Q(sku__icontains=q))
        if categoria.isdigit():
            qs = qs.filter(categoria_id=int(categoria))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categorias"] = Categoria.objects.all()
        ctx["q"] = self.request.GET.get("q", "")
        ctx["categoria_sel"] = self.request.GET.get("categoria", "")
        return ctx


class ProductoCreateView(RolRequeridoMixin, SuccessMessageMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    permission_required = "inventario.add_producto"
    success_url = reverse_lazy("producto_list")
    success_message = "Producto creado correctamente."

    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        return super().form_valid(form)


class ProductoUpdateView(RolRequeridoMixin, SuccessMessageMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    permission_required = "inventario.change_producto"
    success_url = reverse_lazy("producto_list")
    success_message = "Producto actualizado correctamente."


class ProductoDeleteView(RolRequeridoMixin, DeleteView):
    model = Producto
    permission_required = "inventario.delete_producto"
    success_url = reverse_lazy("producto_list")

    def form_valid(self, form):
        messages.success(self.request, "Producto eliminado correctamente.")
        return super().form_valid(form)


# --------------------------------------------------------------------------
# CRUD de Categorías
# --------------------------------------------------------------------------
class CategoriaListView(RolRequeridoMixin, ListView):
    model = Categoria
    permission_required = "inventario.view_categoria"

    def get_queryset(self):
        return Categoria.objects.annotate(num_productos=Count("productos"))


class CategoriaCreateView(RolRequeridoMixin, SuccessMessageMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    permission_required = "inventario.add_categoria"
    success_url = reverse_lazy("categoria_list")
    success_message = "Categoría creada correctamente."


class CategoriaUpdateView(RolRequeridoMixin, SuccessMessageMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    permission_required = "inventario.change_categoria"
    success_url = reverse_lazy("categoria_list")
    success_message = "Categoría actualizada correctamente."


class CategoriaDeleteView(RolRequeridoMixin, DeleteView):
    model = Categoria
    permission_required = "inventario.delete_categoria"
    success_url = reverse_lazy("categoria_list")

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                "No se puede eliminar: la categoría tiene productos asociados.",
            )
            return redirect("categoria_list")
        messages.success(self.request, "Categoría eliminada correctamente.")
        return response


# --------------------------------------------------------------------------
# Reportes / Dashboard (agregaciones del ORM)
# --------------------------------------------------------------------------
class ReporteView(RolRequeridoMixin, TemplateView):
    template_name = "inventario/reporte.html"
    permission_required = "inventario.view_producto"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        valor_expr = ExpressionWrapper(F("precio") * F("stock"), output_field=VALOR)

        # 1) Métricas globales con aggregate()
        ctx["resumen"] = Producto.objects.aggregate(
            total_productos=Count("id"),
            total_unidades=Coalesce(Sum("stock"), 0),
            precio_promedio=Avg("precio"),
            valor_total=Coalesce(Sum(valor_expr), Value(Decimal("0")), output_field=VALOR),
        )

        # 2) Resumen por categoría con annotate()
        por_categoria = Categoria.objects.annotate(
            num_productos=Count("productos"),
            unidades=Coalesce(Sum("productos__stock"), 0),
            valor=Coalesce(
                Sum(F("productos__precio") * F("productos__stock"), output_field=VALOR),
                Value(Decimal("0")),
                output_field=VALOR,
            ),
        ).order_by("-valor")
        ctx["por_categoria"] = por_categoria

        # 3) Top 5 productos por valor de inventario
        ctx["top_productos"] = (
            Producto.objects.select_related("categoria")
            .annotate(valor=valor_expr)
            .order_by("-valor")[:5]
        )

        # 4) Productos con stock crítico (stock <= stock mínimo)
        ctx["stock_critico"] = (
            Producto.objects.select_related("categoria")
            .filter(stock__lte=F("stock_minimo"))
            .order_by("stock")
        )

        # Datos para el gráfico (se entregan con json_script en la plantilla)
        ctx["chart_data"] = {
            "labels": [c.nombre for c in por_categoria],
            "valores": [float(c.valor) for c in por_categoria],
            "unidades": [int(c.unidades) for c in por_categoria],
        }
        return ctx
