# Guía de Diapositivas para Presentación del Proyecto UNACH-LA
## Resumen Ordenado por Carpetas, Notebooks y Archivos JSON

---

### Diapositiva 1: Portada y Visión Institucional
- **Título**: Sistema de Alerta Temprana UNACH-LA mediante Inteligencia Artificial.
- **Objetivo**: Predecir el riesgo de reprobación y optimizar la intervención pedagógica tutorial.

---

### Diapositiva 2: Carpeta 1 - Preprocesamiento (`Diseño e Implementación ML`)
- **Población**: 4,000 estudiantes procesados.
- **Resultado Clave**: Base de datos limpia y sin nulos (`dataset_procesado.csv`).

---

### Diapositiva 3: Carpeta 2 - Evaluación de Modelos (`Evaluación de Modelos`)
- **Notebook**: `Evaluacion_y_Validacion_Modelos.ipynb`
- **JSON Obtenido**: `resultados_evaluacion.json`
- **Comparativa de Rendimiento**:
  - **XGBoost Classifier**: F1-Score = 0.4952, ROC-AUC = 0.7042 (Modelo seleccionado).
  - **Random Forest**: F1-Score = 0.4720.

---

### Diapositiva 4: Carpeta 3 - Visualización y KPIs (`Visualización y KPIs`)
- **Notebook**: `Propuesta_KPIs_y_Dashboards.ipynb`
- **JSON Obtenido**: `kpis_academicos.json`
- **Indicadores Clave**:
  - **Tasa Global de Riesgo**: 46.98% (Semaforización Crítica).
  - **Rendimiento Promedio**: 7.16 / 10.
  - **Asistencia Promedio**: 85.0%.

---

### Diapositiva 5: Carpeta 4 - Prototipo Funcional Completo (`Fase 3 - Documentación y Cierre`)
- **Notebook**: `Prototipo_Funcional_UNACH_LA.ipynb`
- **JSON Obtenido**: `alertas_unach_la.json`
- **Semaforización y Acción Tutorial**:
  - 🔴 **Riesgo Alto (47.0%)**: Tutoría académica obligatoria y derivación a Bienestar.
  - 🟢 **Riesgo Bajo (53.0%)**: Seguimiento regular de aula.
