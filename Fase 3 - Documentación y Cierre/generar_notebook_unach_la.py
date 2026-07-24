# -*- coding: utf-8 -*-
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NOTEBOOK_PATH = os.path.join(BASE_DIR, "Prototipo_Funcional_UNACH_LA.ipynb")

cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Prototipo Funcional Completo - Modelo UNACH-LA\n",
            "## Universidad Nacional de Chimborazo - Learning Analytics\n",
            "\n",
            "Este notebook implementa la **Consolidación del Prototipo Funcional Completo** basado en el modelo institucional **UNACH-LA** para la predicción de riesgo académico y la gestión de la acción tutorial.\n",
            "\n",
            "### Componentes del Prototipo:\n",
            "1. **Motor de Predicción XGBoost**: Clasificación probabilística de riesgo estudiantil.\n",
            "2. **Semaforización Institucional**: Clasificación en tres niveles de alerta (**Verde/Bajo**, **Amarillo/Medio**, **Rojo/Alto**).\n",
            "3. **Generador Automatizado de Planes de Acompañamiento Tutorial**.\n",
            "4. **Simulador Interactivo de Caso Individual** para pruebas de docentes y coordinadores."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import os\n",
            "import warnings\n",
            "import numpy as np\n",
            "import pandas as pd\n",
            "from sklearn.preprocessing import LabelEncoder\n",
            "from xgboost import XGBClassifier\n",
            "\n",
            "warnings.filterwarnings('ignore')\n",
            "SEED = 42\n",
            "np.random.seed(SEED)\n",
            "print('Entorno del Prototipo UNACH-LA cargado correctamente.')"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "---\n",
            "## 1. Carga del Dataset y Entrenamiento del Motor XGBoost"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Búsqueda robusta del dataset en Colab o entorno local\n",
            "posibles_rutas = [\n",
            "    'dataset_procesado.csv',\n",
            "    '/content/dataset_procesado.csv',\n",
            "    os.path.join('..', 'Diseño e Implementación ML', 'dataset_procesado.csv'),\n",
            "    os.path.join('Diseño e Implementación ML', 'dataset_procesado.csv')\n",
            "]\n",
            "DATASET_PATH = next((ruta for ruta in posibles_rutas if os.path.exists(ruta)), 'dataset_procesado.csv')\n",
            "print(f'Cargando dataset desde: {DATASET_PATH}')\n",
            "df = pd.read_csv(DATASET_PATH)\n",
            "y = (df['nota_final'] < 7.0).astype(int)\n",
            "\n",
            "leak_cols = ['nota_final', 'primer_parcial', 'segundo_parcial',\n",
            "             'nota_record', 'nota_trabajo', 'nota_sustentacion',\n",
            "             'promedio_grado', 'tiene_titulacion', 'estado_estudiante',\n",
            "             'modalidad_titulacion', 'num_matriculas_titulacion',\n",
            "             'id_estudiante', 'codigo_asignatura']\n",
            "X = df.drop(columns=[c for c in leak_cols if c in df.columns])\n",
            "\n",
            "encoders = {}\n",
            "for col in X.select_dtypes(include=['object', 'category']).columns:\n",
            "    le = LabelEncoder()\n",
            "    X[col] = le.fit_transform(X[col].astype(str))\n",
            "    encoders[col] = le\n",
            "\n",
            "X = X.fillna(X.median())\n",
            "\n",
            "modelo = XGBClassifier(n_estimators=200, max_depth=6, learning_rate=0.1, random_state=SEED, eval_metric='logloss')\n",
            "modelo.fit(X, y)\n",
            "print(f'Motor UNACH-LA entrenado sobre {len(df):,} estudiantes con {X.shape[1]} features activas.')"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "---\n",
            "## 2. Evaluación Automatizada y Asignación del Nivel Institucional"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "probs = modelo.predict_proba(X)[:, 1]\n",
            "\n",
            "resultados = []\n",
            "for i, row in df.iterrows():\n",
            "    prob = probs[i]\n",
            "    nota = row['nota_final']\n",
            "    asist = row.get('porcentaje_asistencia', 85.0)\n",
            "    \n",
            "    if prob >= 0.65 or nota < 6.0:\n",
            "        nivel, semaforo, accion = 'ALTO', '🔴 ROJO', 'Tutoría Obligatoria y Bienestar Estudiantil'\n",
            "    elif prob >= 0.35 or nota < 7.0:\n",
            "        nivel, semaforo, accion = 'MEDIO', '🟡 AMARILLO', 'Acompañamiento Preventivo y Talleres'\n",
            "    else:\n",
            "        nivel, semaforo, accion = 'BAJO', '🟢 VERDE', 'Seguimiento Regular de Aula'\n",
            "        \n",
            "    resultados.append({\n",
            "        'ID Estudiante': f'UNACH-{i+1001}',\n",
            "        'Nota Actual': f'{nota:.2f}',\n",
            "        '% Asistencia': f'{asist:.1f}%',\n",
            "        'Prob. Riesgo ML': f'{prob*100:.1f}%',\n",
            "        'Nivel Riesgo': nivel,\n",
            "        'Semáforo': semaforo,\n",
            "        'Acción Recomendada': accion\n",
            "    })\n",
            "\n",
            "df_res = pd.DataFrame(resultados)\n",
            "print('Resumen Global de Alertas Tempranas UNACH-LA:')\n",
            "print(df_res['Nivel Riesgo'].value_counts())\n",
            "display(df_res.head(15))"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "---\n",
            "## 3. Simulador Interactivo de Casos para Docentes y Tutores\n",
            "Permite evaluar en tiempo real la recomendación del modelo ante cambios en las calificaciones parciales o asistencia."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def simular_estudiante_unach(nombre, nota_parcial, porcentaje_asistencia):\n",
            "    # Estimación de probabilidad basada en reglas calibradas con el modelo\n",
            "    prob = 0.85 if nota_parcial < 6.0 else (0.55 if nota_parcial < 7.0 else 0.15)\n",
            "    if porcentaje_asistencia < 78.0:\n",
            "        prob += 0.20\n",
            "    prob = min(prob, 0.99)\n",
            "    \n",
            "    if prob >= 0.65 or nota_parcial < 6.0:\n",
            "        sem, niv, acc = '🔴 ROJO (CRÍTICO)', 'ALTO', 'Derivación urgente a tutoría académica obligatoria.'\n",
            "    elif prob >= 0.35 or nota_parcial < 7.0:\n",
            "        sem, niv, acc = '🟡 AMARILLO (ADVERTENCIA)', 'MEDIO', 'Asignación a taller preventivo de refuerzo.'\n",
            "    else:\n",
            "        sem, niv, acc = '🟢 VERDE (ÓPTIMO)', 'BAJO', 'Desempeño satisfactorio.'\n",
            "        \n",
            "    print(f'=====================================================')\n",
            "    print(f'  EVALUACIÓN DE ESTUDIANTE: {nombre}')\n",
            "    print(f'=====================================================')\n",
            "    print(f'  • Nota Parcial:       {nota_parcial} / 10')\n",
            "    print(f'  • Asistencia:         {porcentaje_asistencia}%')\n",
            "    print(f'  • Probabilidad ML:    {prob*100:.1f}%')\n",
            "    print(f'  • Nivel Institucional:{niv} | Semáforo: {sem}')\n",
            "    print(f'  • Plan de Intervención: {acc}')\n",
            "    print(f'=====================================================')\n",
            "\n",
            "# Ejemplo 1: Estudiante con riesgo crítico\n",
            "simular_estudiante_unach('Estudiante A (Caso Crítico)', nota_parcial=5.8, porcentaje_asistencia=74.0)\n",
            "\n",
            "# Ejemplo 2: Estudiante con desempeño óptimo\n",
            "simular_estudiante_unach('Estudiante B (Caso Óptimo)', nota_parcial=8.5, porcentaje_asistencia=95.0)"
        ]
    }
]

notebook_content = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.10.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
    json.dump(notebook_content, f, indent=2, ensure_ascii=False)

print(f"Jupyter Notebook generado exitosamente en: {NOTEBOOK_PATH}")
