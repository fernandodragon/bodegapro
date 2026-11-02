# Guion de presentación (≈ 10-12 min)

## 1. Introducción (1 min)
TechLogix necesita controlar su inventario. Qué hace la app y quién la usa (Administrador y Asistente).

## 2. Arquitectura Django (2 min)
- Proyecto `config` + app `inventario`.
- Modelos: `Categoria` 1—N `Producto` (FK con `PROTECT`), validadores de SKU y precio.
- Vistas basadas en clases con `LoginRequiredMixin` + permisos; consultas con `select_related`.
- PostgreSQL en la nube mediante `DATABASE_URL`.

## 3. Demo en vivo sobre la URL de producción (5 min)
Ensayar el flujo completo antes:
1. Registrarse con un usuario nuevo → queda como **Asistente**: ve productos y reportes, no ve botones de editar.
2. Intentar abrir `/productos/nuevo/` → mensaje de falta de permisos.
3. Cerrar sesión e iniciar como **Administrador**.
4. Crear un producto (mostrar una validación con error), editarlo y eliminarlo.
5. Intentar borrar una categoría con productos → protección `PROTECT`.
6. Abrir **Reportes**: KPIs, gráficos, top 5 y stock crítico. Crear un producto con stock bajo y recargar para ver el cambio.

## 4. Despliegue y seguridad (1 min)
`DEBUG=False`, `SECRET_KEY` y BD en variables de entorno, WhiteNoise para estáticos, HTTPS.

## 5. Costos e IA (2-3 min)
Mostrar la tabla resumen de `INFORME_COSTOS.md`: HH, infraestructura, IA, total y ahorro.
Explicar la metodología (horas × tarifa, precios de Render, tipo de cambio) y el análisis crítico de la IA.

## Preguntas que pueden hacerte
- ¿Qué es `select_related` y por qué lo usaron?
- ¿Cómo evitan que un Asistente edite productos si conoce la URL?
- ¿Qué diferencia hay entre `aggregate` y `annotate`?
- ¿Por qué `on_delete=PROTECT`?
- ¿Qué parte del código generó la IA y cómo la revisaron?
