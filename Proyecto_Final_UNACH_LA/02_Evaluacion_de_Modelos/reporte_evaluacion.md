# Reporte de Evaluación de Modelos
## Evaluación de Modelos - Validación y Pruebas de Rendimiento

**Fecha de generación**: 2026-07-10 13:52:24
**Entregable**: Resultados de métricas y validación

---

## 1. Configuración del Experimento

| Parámetro | Valor |
|-----------|-------|
| Total de registros | 4,000 |
| Train set | 3,200 (80%) |
| Test set | 800 (20%) |
| Features | 66 |
| Validación cruzada | 5-Fold Stratified |
| Semilla aleatoria | 42 |
| Escalado | StandardScaler (LR, SVM) |

### Distribución del Target

| Clase | Train | Test | Total |
|-------|-------|------|-------|
| En riesgo (1) | 1,503 | 376 | 1,879 |
| Sin riesgo (0) | 1,697 | 424 | 2,121 |

---

## 2. Resultados de Validación Cruzada (5-Fold)

| Modelo | Accuracy | Precision | Recall | F1-Score | AUC-ROC |
|--------|----------|-----------|--------|----------|---------|
| Logistic Regression | 0.5094 ±0.0153 | 0.4717 ±0.0213 | 0.3540 ±0.0101 | 0.4040 ±0.0060 | 0.5122 ±0.0209 |
| Decision Tree | 0.5203 ±0.0198 | 0.4883 ±0.0223 | 0.4358 ±0.0607 | 0.4585 ±0.0377 | 0.5251 ±0.0273 |
| Random Forest | 0.5162 ±0.0098 | 0.4816 ±0.0134 | 0.3899 ±0.0166 | 0.4307 ±0.0134 | 0.5089 ±0.0122 |
| XGBoost | 0.5100 ±0.0200 | 0.4765 ±0.0230 | 0.4278 ±0.0142 | 0.4507 ±0.0169 | 0.5089 ±0.0165 |
| SVM | 0.5188 ±0.0171 | 0.4839 ±0.0260 | 0.3447 ±0.0291 | 0.4017 ±0.0218 | 0.5149 ±0.0173 |

---

## 3. Resultados en Conjunto de Test

| Modelo | Accuracy | Precision | Recall | F1-Score | AUC-ROC | Avg Precision | Specificity |
|--------|----------|-----------|--------|----------|---------|---------------|-------------|
| Logistic Regression | 0.5200 | 0.4852 | 0.3484 | 0.4056 | 0.5137 | 0.4743 | 0.6722 |
| Decision Tree | 0.4938 | 0.4607 | 0.4521 | 0.4564 | 0.5048 | 0.4725 | 0.5307 |
| Random Forest | 0.5200 | 0.4869 | 0.3963 | 0.4370 | 0.5120 | 0.4868 | 0.6297 |
| XGBoost **★** | 0.5437 | 0.5159 | 0.4761 | 0.4952 | 0.5314 | 0.4932 | 0.6038 |
| SVM | 0.5162 | 0.4801 | 0.3537 | 0.4074 | 0.5014 | 0.4591 | 0.6604 |

> **★ Mejor modelo por F1-Score: XGBoost**

---

## 4. Matrices de Confusión

| Modelo | TN (Verdaderos Neg.) | FP (Falsos Pos.) | FN (Falsos Neg.) | TP (Verdaderos Pos.) |
|--------|---------------------|-------------------|-------------------|----------------------|
| Logistic Regression | 285 | 139 | 245 | 131 |
| Decision Tree | 225 | 199 | 206 | 170 |
| Random Forest | 267 | 157 | 227 | 149 |
| XGBoost | 256 | 168 | 197 | 179 |
| SVM | 280 | 144 | 243 | 133 |

---

## 5. Análisis de Overfitting

| Modelo | Train Accuracy | Test Accuracy (CV) | Diferencia | Diagnóstico |
|--------|---------------|--------------------|-----------:|-------------|
| Logistic Regression | 0.5645 | 0.5094 | 0.0552 | ⚡ Overfitting moderado |
| Decision Tree | 0.7633 | 0.5203 | 0.2430 | ⚠️ Overfitting alto |
| Random Forest | 0.9998 | 0.5162 | 0.4836 | ⚠️ Overfitting alto |
| XGBoost | 1.0000 | 0.5100 | 0.4900 | ⚠️ Overfitting alto |
| SVM | 0.8470 | 0.5188 | 0.3282 | ⚠️ Overfitting alto |

---

## 6. Top-15 Variables Más Importantes

| # | Variable | Importancia |
|---|----------|-------------|
| 1 | `comp_cuestionario` | 0.021264 |
| 2 | `franja_preferida` | 0.020603 |
| 3 | `evt_quiz_submitted` | 0.020533 |
| 4 | `comp_foro` | 0.020271 |
| 5 | `tiempo_conexion_promedio_min` | 0.020060 |
| 6 | `comp_tarea` | 0.020039 |
| 7 | `evt_page_viewed` | 0.019863 |
| 8 | `duracion_total_seg` | 0.019491 |
| 9 | `actividad_finde` | 0.019361 |
| 10 | `sector_residencia` | 0.019328 |
| 11 | `calificacion_lms_min` | 0.019261 |
| 12 | `evt_quiz_attempted` | 0.018796 |
| 13 | `navegador_principal` | 0.018749 |
| 14 | `tasa_errores` | 0.018534 |
| 15 | `dias_activos` | 0.018287 |

---

## 7. Conclusiones

### Mejor Modelo: **XGBoost**

| Métrica | Valor |
|---------|-------|
| Accuracy | 0.5437 |
| Precision | 0.5159 |
| Recall | 0.4761 |
| F1-Score | 0.4952 |
| AUC-ROC | 0.5314 |

### Observaciones
- Se evaluaron 5 modelos de clasificación para predecir riesgo académico.
- La validación cruzada (5-Fold) se utilizó para estimar el rendimiento generalizado.
- Las métricas clave son: AUC-ROC (capacidad discriminativa), Precision (evitar falsos positivos),
  Recall (capturar estudiantes en riesgo), y F1-Score (balance precision-recall).
- Se generaron 9 gráficos de evaluación en la carpeta `graficos/`.

---

## 8. Gráficos Generados

| # | Archivo | Descripción |
|---|---------|-------------|
| 1 | `01_tabla_metricas.png` | Tabla comparativa de todas las métricas |
| 2 | `02_matrices_confusion.png` | Matrices de confusión por modelo |
| 3 | `03_curvas_roc.png` | Curvas ROC con AUC |
| 4 | `04_curvas_precision_recall.png` | Curvas Precision-Recall |
| 5 | `05_comparacion_metricas.png` | Barras agrupadas de métricas |
| 6 | `06_cv_boxplot.png` | Distribución CV por fold |
| 7 | `07_overfitting_check.png` | Train vs Test (overfitting) |
| 8 | `08_feature_importance.png` | Top-20 features más importantes |
| 9 | `09_radar_chart.png` | Radar chart multidimensional |

---

*Reporte generado automáticamente por el pipeline de Evaluación de Modelos.*
