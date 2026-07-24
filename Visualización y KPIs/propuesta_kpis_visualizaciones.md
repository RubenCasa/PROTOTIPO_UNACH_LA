# Propuesta de KPIs y Visualizaciones para el Sistema de Alerta Temprana
## Diseño de Dashboards e Indicadores Clave de Desempeño Académico

**Fecha de emisión**: 2026-07-24  
**Entregable**: Propuesta de KPIs y visualizaciones (`Visualización y KPIs`)

---

## 1. Marco Conceptual de Indicadores Clave (KPIs)

El sistema de alerta temprana basado en Inteligencia Artificial requiere un monitoreo continuo de indicadores clave que permitan a coordinadores, directores de carrera y docentes tutores tomar decisiones preventivas eficaces.

### Tabla Resumen de KPIs Institucionales

| Código | Indicador | Definición / Fórmula | Meta Institucional | Valor Actual | Estado |
|--------|-----------|----------------------|--------------------|--------------|--------|
| **KPI-01** | **Tasa Global de Riesgo** | `(Estudiantes < 7.0 / Total Estudiantes) * 100` | `< 25%` | **46.98%** | CRÍTICO |
| **KPI-02** | **Promedio de Calificaciones** | Promedio aritmético de `nota_final` | `>= 7.8 / 10` | **7.16** | ADVERTENCIA |
| **KPI-03** | **Asistencia Promedio** | Promedio del porcentaje de asistencia | `>= 80%` | **85.0%** | ÓPTIMO |
| **KPI-04** | **Efectividad Predictiva ML** | F1-Score del modelo óptimo (XGBoost) | `>= 0.45` | **0.4952** | ÓPTIMO |

---

## 2. Catálogo de Dashboards Visuales Diseñados

Los siguientes paneles han sido creados y se encuentran disponibles en la carpeta `dashboards/`:

1. **`01_tarjetas_kpis_ejecutivos.png`**: Tarjetas ejecutivas de alto impacto visual con semaforización para la dirección académica.
2. **`02_tasa_riesgo_por_carrera.png`**: Ranking comparativo por carrera respecto al umbral institucional del 25%.
3. **`03_asistencia_vs_rendimiento.png`**: Análisis bidimensional para identificar cuadrantes críticos (baja asistencia y bajo rendimiento).
4. **`04_distribucion_notas_riesgo.png`**: Curva de densidad de calificaciones evidenciando la zona crítica de reprobación.
5. **`05_embudo_alerta_temprana.png`**: Embudo operativo para priorizar el número de estudiantes a canalizar hacia tutorías.
6. **`06_dashboard_integral_gestion.png`**: Panel de control general de 4 cuadrantes para seguimiento por periodo académico.

---

## 3. Protocolo de Acción Operativa (Semaforización)

- 🟢 **Óptimo (Verde)**: Desempeño dentro de las metas institucionales. Monitoreo regular.
- 🟡 **Advertencia (Amarillo)**: Tasa de riesgo entre 25% y 35%. Requiere notificación automática al docente y tutor asignado.
- 🔴 **Crítico (Rojo)**: Estudiante o carrera con riesgo > 35% o nota < 6.0. Requiere intervención tutorial inmediata y plan de acompañamiento académico.

---
*Documento generado por el pipeline analítico de Visualización y KPIs.*
