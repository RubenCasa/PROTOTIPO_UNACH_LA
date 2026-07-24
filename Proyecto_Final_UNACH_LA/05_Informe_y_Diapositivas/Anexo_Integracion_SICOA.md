# Anexo: Integración del Sistema Institucional (SICOA) y el Motor ML UNACH-LA

## 1. Contexto de la Brecha
El Sistema Integrado de Control Académico (SICOA) de la Universidad Nacional de Chimborazo (UNACH) centraliza los historiales académicos, notas y asistencias de los estudiantes. Sin embargo, existe una brecha natural entre estos datos crudos almacenados relacionalmente y la capacidad analítica y predictiva necesaria para identificar estudiantes en riesgo académico temprano.

**El Dashboard UNACH-LA** cierra esta brecha funcionando como la capa de inteligencia (Learning Analytics) encima de la infraestructura existente.

## 2. Arquitectura de Integración
Para resolver la interoperabilidad entre SICOA y el motor de Machine Learning (XGBoost):

1. **Extracción (SICOA):** El SICOA exporta periódicamente o bajo demanda los registros consolidados en formatos estructurados universales (`.csv` o `.xlsx`).
2. **Ingesta (Dashboard):** A través del módulo **"Motor ML"**, los coordinadores de carrera o bienestar estudiantil pueden cargar el dataset crudo extraído del SICOA mediante una interfaz de "Drag & Drop".
3. **Procesamiento y Predicción:** 
   - El sistema analiza y transforma los datos entrantes (Feature Engineering).
   - El modelo de predicción pre-entrenado (XGBoost) clasifica a cada estudiante y asigna una probabilidad de deserción o riesgo académico (Score ML).
4. **Visualización y Acción:** Los resultados procesados alimentan la base del Dashboard React. Se actualizan automáticamente los semáforos, el porcentaje global de riesgo y se emiten alertas nominales.

## 3. Demostración en el Prototipo
En el prototipo funcional actual, este flujo se demuestra a través de la pestaña **"Motor ML (SICOA)"**.
- El usuario arrastra un archivo de prueba.
- El sistema simula el Pipeline de inferencia, mostrando estados reactivos de "Cargando" y procesando las variables.
- Finalmente, se emite una respuesta de éxito confirmando que los semáforos de advertencia en las pestañas "Vista General" y "Alertas Críticas" han sido recalibrados.
