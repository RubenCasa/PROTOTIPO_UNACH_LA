# PROYECTO DE INNOVACIÓN: MODELO UNACH-LA
**CÓDIGO:** VERSIÓN: 01
**FECHA:** 26/05/2025 (Actualizado: 24/07/2026)

## 1. ARTICULACIÓN Y PERTINENCIA
El proyecto UNACH-LA se articula de manera directa con la problemática institucional relacionada con la fragmentación y subutilización de los datos académicos, proponiendo una solución escalable y replicable que fortalece la toma de decisiones basadas en evidencia. Su implementación no solo impacta a la UNACH, sino que genera un referente metodológico y tecnológico transferible a otras instituciones de educación superior públicas del país.

- **Dominios académicos:** Desarrollo socioeconómico y educativo para el fortalecimiento de la institucionalidad democrática y ciudadana.
- **Campos del conocimiento:** Educación, Tecnologías de la información y la comunicación (TICs).
- **Líneas de investigación:** Ciencias de la educación, Ingeniería informática.
- **Alineación ODS:** Educación de calidad (ODS 4), Industria, innovación e infraestructura (ODS 9), Alianzas para lograr los objetivos (ODS 17).

## 2. ANÁLISIS DE PROBLEMA, JUSTIFICACIÓN Y DIAGNÓSTICO
### 2.1. Diagnóstico
En la Universidad Nacional de Chimborazo (UNACH), los datos estudiantiles y de rendimiento se encuentran depositados en diferentes plataformas (SICOA, aulas virtuales, tutorías). Uno de los factores limitantes es la brecha digital (aprox. 36% de hogares sin internet estable en Chimborazo). Actualmente, los datos no se integran en un sistema de gobernanza institucional para la toma de decisiones oportunas frente al bajo rendimiento o deserción.

### 2.2. Problema Identificado
Falta de un modelo institucional de analítica del aprendizaje (Learning Analytics) que integre los flujos de datos. Esto genera silos tecnológicos, decisiones basadas en percepciones y la imposibilidad de anticipar el abandono estudiantil.

### 2.3. Justificación
La implementación de UNACH-LA permite consolidar una cultura de mejora continua basada en datos, respondiendo a la política nacional de transformación digital. Convierte la fragmentación de datos en una oportunidad de innovación educativa sustentable.

## 3. RESUMEN EJECUTIVO
El proyecto propone un modelo institucional de analítica del aprendizaje (UNACH-LA) combinando análisis de datos de plataformas (SICOA, Moodle) con modelos predictivos de Machine Learning.
**Novedades Tecnológicas Implementadas (Fase Final):**
- **Arquitectura Empresarial (Backend):** Implementación de un servidor robusto en Python (FastAPI) para gestionar las predicciones e integración con Inteligencia Artificial.
- **Interfaz Institucional (Frontend):** Rediseño total del Dashboard a un "Light Mode" corporativo, alineado con los colores institucionales de la UNACH.
- **Carga de Datos Flexibles:** Incorporación de lectura nativa de archivos CSV y Excel para análisis directos de listados del SICOA.
- **Factor WOW:** Modal 360° de estudiantes y proyecciones gráficas longitudinales de riesgo.

## 4. OBJETIVOS
**Objetivo General:**
Desarrollar e implementar un modelo institucional de Learning Analytics en la UNACH que mejore los procesos de formación, fortalezca las decisiones pedagógicas y transfiera conocimiento.

## 5. METODOLOGÍA E INNOVACIÓN
**Enfoque Mixto:** Cuantitativo (Minería de datos, modelos predictivos XGBoost, extracción de SICOA) y Cualitativo (Validación, grupos focales).
**Componente de Innovación:**
- **Backend/ETL:** Python, FastAPI, SQL.
- **Analítica:** scikit-learn, XGBoost.
- **Frontend:** React, Vite, Chart.js.
- **Interoperabilidad:** Carga de reportes CSV exportados de SICOA directamente al dashboard.
- **Arquitectura Fallback:** Conexión segura a servicios LLM con simulación local en caso de cortes de red.

## 6. IMPACTO POTENCIAL
- **Impacto Tecnológico:** Sistema institucional UNACH-LA, plataforma interoperable (Machine Learning + Visualización en tiempo real + AI Generativa).
- **Impacto Social:** Beneficio para más de 2000 estudiantes y 200 docentes.
- **Impacto Económico:** Reducción proyectada en costos de repetición y optimización de recursos de nivelación.

## 7. PLAN DE TRANSFERENCIA Y SOSTENIBILIDAD
El software (incluyendo el nuevo Backend en FastAPI y Frontend en React) será gestionado mediante el repositorio institucional. Se tramitará el registro de software en el SENADI. El diseño "Light Mode" institucional facilita la adopción inmediata por parte de las autoridades universitarias (Vicerrectorado Académico y Direcciones de Carrera).
