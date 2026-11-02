# Informe de costos de desarrollo · TechLogix (Django)

> Los valores marcados con (*) son **supuestos editables**: cámbialos por tus datos reales
> (horas que realmente trabajaron, tipo de cambio del día, plan de IA que usaron).

## 1. Costo de horas/hombre (HH)
Tarifa referencial (*): **$8.000 CLP/hora** (desarrollador junior/semi-senior en Chile).

| Actividad | Horas con IA |
|---|---:|
| Análisis y diseño del modelo de datos | 4 |
| Modelos, formularios y CRUD (CBVs) | 8 |
| Autenticación, registro y roles | 5 |
| Reportes y dashboard (agregaciones + gráficos) | 6 |
| Plantillas e interfaz | 6 |
| Despliegue en la nube y variables de entorno | 4 |
| Pruebas y depuración | 5 |
| Documentación y preparación de la presentación | 4 |
| **Total** | **42 h** |

Costo HH con IA: 42 h × $8.000 = **$336.000 CLP**.
Estimación sin IA (*): 68 h × $8.000 = **$544.000 CLP**.

## 2. Costo de infraestructura cloud
Precios de Render consultados en octubre de 2026 (verifica antes de exponer):
Web Service Starter ≈ US$7/mes y PostgreSQL Basic-256 MB ≈ US$6/mes → **US$13/mes**.
Tipo de cambio supuesto (*): $950 CLP/US$.

| Ítem | Cálculo | CLP |
|---|---|---:|
| Desarrollo y evaluación (planes gratuitos de Render) | US$0 | $0 |
| Producción proyectada: web + BD, 12 meses | US$13 × 12 × 950 | $148.200 |
| Dominio .cl (*) | ~ $10.000 / año | $10.000 |
| **Total infraestructura año 1** | | **$158.200** |

Nota: el Postgres gratuito de Render expira, y el web gratuito "se duerme" tras 15 min sin uso;
por eso producción se proyecta con planes de pago.

## 3. Consumo de herramientas de IA
Suscripción a un asistente de IA (*): US$20 × 1 mes × 950 = **$19.000 CLP**.
(Si usaron GitHub Copilot gratis u otra herramienta, ajusta este valor.)

## 4. Resumen

| Concepto | Con IA | Sin IA |
|---|---:|---:|
| Horas/hombre | $336.000 | $544.000 |
| Infraestructura (año 1) | $158.200 | $158.200 |
| Herramientas de IA | $19.000 | $0 |
| **Total** | **$513.200** | **$702.200** |

Ahorro neto: $189.000 CLP (**≈ 27 %**). Si el trabajo se divide entre integrantes, el costo por
persona es el total dividido por el número de integrantes.

## 5. Análisis del impacto de la IA
- **Velocidad:** acelera la estructura repetitiva (modelos, formularios, plantillas, `render.yaml`).
  Se estima una reducción de ~38 % de las horas (68 h → 42 h).
- **Calidad:** ayuda a sugerir buenas prácticas (`select_related`, `PROTECT`, permisos por grupo),
  pero hay que revisar cada pieza: puede inventar parámetros o usar versiones antiguas de Django.
- **Depuración:** útil para interpretar tracebacks y errores de despliegue (migraciones, estáticos,
  `ALLOWED_HOSTS`), siempre verificando la solución en el entorno real.
- **Riesgos:** código que no se entiende no se puede defender en la demo; por eso el equipo debe
  poder explicar cada archivo.
- **Conclusión:** la IA redujo el costo de HH más de lo que costó la herramienta, pero no reemplaza
  el criterio técnico ni las pruebas.
