# TechLogix S.A. · Evaluación 3 Backend (Django)

Aplicación web de inventario con CRUD de **Productos** y **Categorías**, autenticación nativa
de Django con roles (Administrador / Asistente) y un dashboard de reportes con agregaciones del ORM.

## Rúbrica → dónde está cada cosa
| Criterio | Archivo |
|---|---|
| Modelos y relaciones (FK, PROTECT, validadores) | `inventario/models.py` |
| CRUD con CBVs, `select_related`, filtros y paginación | `inventario/views.py` |
| Validaciones en formularios | `inventario/forms.py` |
| Autenticación, registro, `LoginRequiredMixin` + permisos por rol | `inventario/mixins.py`, `views.py`, `management/commands/setup_roles.py` |
| Reportes (`aggregate`, `annotate`, `Count`, `Sum`, `Avg`, `F`) + gráficos | `ReporteView`, `templates/inventario/reporte.html` |
| Despliegue (DEBUG=False, variables de entorno, WhiteNoise) | `config/settings.py`, `build.sh`, `render.yaml` |
| Costos y análisis de IA | `docs/INFORME_COSTOS.md` |
| Guion de presentación y demo | `docs/GUION_PRESENTACION.md` |

## Ejecutar en local (sin entorno virtual)
```bash
pip install -r requirements.txt
copy .env.example .env          # en Windows (en Linux/Mac: cp)
python manage.py migrate
python manage.py setup_roles
python manage.py cargar_demo     # datos de ejemplo
python manage.py createsuperuser
python manage.py runserver
python manage.py test            # pruebas automáticas
```
Para dar rol **Administrador** a un usuario: entra a `/admin/` → Usuarios → Grupos → Administrador.
Los usuarios que se registran solos quedan como **Asistente** (solo lectura).

> Esta versión ya incluye `inventario/migrations/0001_initial.py`, lista para subir a GitHub.

## Despliegue en Render
1. Sube el proyecto a un repositorio de GitHub.
2. En Render: **New → Blueprint** y elige el repo (usa `render.yaml`), o crea a mano un Web Service
   (Build: `./build.sh`, Start: `gunicorn config.wsgi:application`) y una base PostgreSQL.
3. Variables de entorno: `SECRET_KEY` (aleatoria), `DEBUG=False`, `DATABASE_URL` (la de la BD),
   `PYTHON_VERSION=3.12.7`.
4. Abre una Shell en Render y ejecuta `python manage.py createsuperuser` y `python manage.py cargar_demo`.
5. Entrega **solo la URL** pública en la plataforma institucional.

## Uso de IA (para documentar en la presentación)
Completa aquí los prompts reales que usaste, qué te entregó la IA y qué tuviste que corregir.
