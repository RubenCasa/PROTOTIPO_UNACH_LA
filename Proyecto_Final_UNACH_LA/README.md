# 🎓 Proyecto de Investigación UNACH-LA: Sistema de Alerta Temprana con Inteligencia Artificial

[![Universidad Nacional de Chimborazo](https://img.shields.io/badge/UNACH-Learning%20Analytics-blue.svg)](https://www.unach.edu.ec)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://www.python.org/)
[![Machine Learning](https://img.shields.io/badge/ML-XGBoost%20%7C%20Scikit--Learn-orange.svg)](https://xgboost.readthedocs.io/)

Este repositorio contiene la estructura completa del proyecto de **Learning Analytics (UNACH-LA)** y **Sistema de Alerta Temprana** de la Universidad Nacional de Chimborazo, diseñado para predecir oportunamente el riesgo de reprobación e impulsar intervenciones tutoriales preventivas.

---

## 📁 Estructura del Repositorio

```
Repositorio_GitHub_UNACH_LA/
├── 01_Diseno_e_Implementacion_ML/   # Limpieza de datos, imputación y dataset procesado
├── 02_Evaluacion_de_Modelos/        # Notebook de evaluación, script ML y 9 gráficos comparativos
├── 03_Visualizacion_y_KPIs/         # Notebook de KPIs, cálculo de métricas institucionales y dashboards
├── 04_Prototipo_UNACH_LA/           # Prototipo Funcional UNACH-LA con simulador y alertas en JSON/CSV
├── 05_Informe_y_Diapositivas/       # Documento Word (.docx) e informe para armar diapositivas
├── README.md                        # Documentación maestra del repositorio
├── requirements.txt                 # Dependencias del proyecto
└── .gitignore                       # Configuración Git
```

---

## 📓 Notebooks Disponibles (Compatibles con Google Colab y Jupyter Local)

1. `02_Evaluacion_de_Modelos/Evaluacion_y_Validacion_Modelos.ipynb`
2. `03_Visualizacion_y_KPIs/Propuesta_KPIs_y_Dashboards.ipynb`
3. `04_Prototipo_UNACH_LA/Prototipo_Funcional_UNACH_LA.ipynb`

> **Nota para Google Colab**: Cada notebook incluye búsqueda automática del archivo `dataset_procesado.csv`. Puedes subirlo directamente a la carpeta `/content` o en la misma ruta del notebook.

---

## 🚀 Instalación y Ejecución Rápida

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/unach-la-alerta-temprana.git
cd unach-la-alerta-temprana

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Abrir Jupyter Notebooks
jupyter notebook
```

---
*Desarrollado para el Proyecto de Investigación de Ayudantía - Universidad Nacional de Chimborazo (UNACH).*
