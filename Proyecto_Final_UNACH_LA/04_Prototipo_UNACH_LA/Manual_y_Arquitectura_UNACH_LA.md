# Consolidación del Prototipo Funcional y Modelo UNACH-LA
## Universidad Nacional de Chimborazo - Sistema Institucional de Learning Analytics

**Versión del Prototipo**: 1.0 (Prototipo Funcional Completo)  
**Fecha de Consolidación**: 2026-07-10  
**Entregable**: `Fase 3: Documentación y Cierre`

---

## 1. Arquitectura y Modelo Institucional UNACH-LA

El modelo **UNACH-LA (Learning Analytics)** articula los datos procedentes del Sistema Integrado de Componente Académico (SICOA) y plataformas LMS para predecir oportunamente el riesgo de reprobación y deserción en las asignaturas de la universidad.

```
+-------------------------------------------------------------------------------+
|                        ARQUITECTURA DEL MODELO UNACH-LA                       |
+-------------------------------------------------------------------------------+
|  1. FUENTES DE DATOS         2. MOTOR PREDICTIVO (ML)  3. ACCIÓN PEDAGÓGICA   |
|                                                                               |
|  +--------------------+      +--------------------+    +-------------------+  |
|  | SICOA (Notas /     | ---> | Preprocesamiento y | -> | Alertas Tempranas |  |
|  | Asistencia / Malla)|      | Feature Engineering|    | (Semaforización)  |  |
|  +--------------------+      +--------------------+    +-------------------+  |
|                                        |                         |            |
|  +--------------------+      +--------------------+    +-------------------+  |
|  | LMS (Actividad en  | ---> | Modelo XGBoost     | -> | Planes de Tutoría |  |
|  | Aula Virtual)      |      | Calibrado          |    | Personalizados    |  |
|  +--------------------+      +--------------------+    +-------------------+  |
+-------------------------------------------------------------------------------+
```

---

## 2. Resultados de Evaluación en la Población Estudiantil

El prototipo funcional se ejecutó sobre **4,000 estudiantes**, obteniendo la siguiente distribución operativa de riesgo y priorización tutorial:

| Nivel de Riesgo | Semáforo | N° de Estudiantes | Porcentaje | Acción Institucional Recomendada |
|:---:|:---:|:---:|:---:|:---|
| **ALTO** | 🔴 **ROJO (CRÍTICO)** | **1,831** | **45.8%** | Tutoría académica obligatoria y derivación a Bienestar Estudiantil. |
| **MEDIO** | 🟡 **AMARILLO (ADVERTENCIA)** | **111** | **2.8%** | Acompañamiento preventivo y talleres de refuerzo. |
| **BAJO** | 🟢 **VERDE (ÓPTIMO)** | **2,058** | **51.4%** | Seguimiento regular en aula. |

---

## 3. Estructura y Salidas del Prototipo

El sistema genera de forma automatizada dos entregables de interoperabilidad institucional:
1. **Reporte Detallado CSV (`estudiantes_evaluados_unach_la.csv`)**: Contiene el listado completo nominal con su probabilidad de riesgo por estudiante y su plan de acción asignado.
2. **Alertas en Formato JSON (`alertas_unach_la.json`)**: Archivo consumible por portales web docentes o APIs universitarias.

---

## 4. Guía Operativa para Coordinadores y Docentes Tutores

1. **Revisión Semanal de Alertas Rojas**: Priorizar a los estudiantes identificados en nivel **ALTO** durante las primeras 4 semanas del ciclo académico.
2. **Plan de Acción Personalizado**: Aplicar las recomendaciones generadas por el prototipo (`plan_acompanamiento`).
3. **Registro de Eficacia**: Monitorear el progreso en el segundo parcial para comprobar la reducción del nivel de riesgo.

---
*Prototipo Funcional Completo desarrollado para el Proyecto de Investigación de Ayudantía - UNACH.*
