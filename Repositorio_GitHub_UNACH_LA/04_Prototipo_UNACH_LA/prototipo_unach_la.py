# -*- coding: utf-8 -*-
"""
PROTOTIPO FUNCIONAL COMPLETO - MODELO UNACH-LA (Learning Analytics)
===================================================================
Universidad Nacional de Chimborazo (UNACH) - Sistema de Alerta Temprana
Consolidación del Prototipo Funcional de Predicción e Intervención Tutorial.
"""

import os
import sys
import io
import json
import warnings
from datetime import datetime
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from xgboost import XGBClassifier

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
warnings.filterwarnings('ignore')

# Rutas del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
DATASET_PATH = os.path.join(PROJECT_DIR, "Diseño e Implementación ML", "dataset_procesado.csv")
EXPORT_CSV_PATH = os.path.join(BASE_DIR, "estudiantes_evaluados_unach_la.csv")
EXPORT_JSON_PATH = os.path.join(BASE_DIR, "alertas_unach_la.json")
MANUAL_PATH = os.path.join(BASE_DIR, "Manual_y_Arquitectura_UNACH_LA.md")

SEED = 42
np.random.seed(SEED)

class PrototipoUNACHLA:
    """
    Motor del Prototipo Funcional UNACH-LA:
    - Entrena/gestiona modelo clasificador XGBoost.
    - Calcula probabilidad de riesgo académico.
    - Asigna nivel de riesgo (Bajo, Medio, Alto).
    - Genera recomendaciones de acción tutorial automatizada.
    """
    def __init__(self):
        self.modelo = None
        self.feature_names = None
        self.encoders = {}
        self.scaler = StandardScaler()
        
    def entrenar_motor(self, df):
        print("  >> Entrenando motor analítico UNACH-LA (XGBoost Classifier)...")
        # Definir target
        y = (df['nota_final'] < 7.0).astype(int)
        
        # Eliminar data leakage e ids
        leak_cols = ['nota_final', 'primer_parcial', 'segundo_parcial',
                     'nota_record', 'nota_trabajo', 'nota_sustentacion',
                     'promedio_grado', 'tiene_titulacion', 'estado_estudiante',
                     'modalidad_titulacion', 'num_matriculas_titulacion',
                     'id_estudiante', 'codigo_asignatura']
        X = df.drop(columns=[c for c in leak_cols if c in df.columns])
        
        # Codificación
        cat_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()
        for col in cat_cols:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            self.encoders[col] = le
            
        X = X.fillna(X.median())
        self.feature_names = X.columns.tolist()
        
        self.modelo = XGBClassifier(
            n_estimators=200, max_depth=6, learning_rate=0.1,
            random_state=SEED, eval_metric='logloss'
        )
        self.modelo.fit(X, y)
        print(f"  >> Motor calibrado exitosamente con {len(self.feature_names)} variables predictivas.")
        return X, y
        
    def generar_plan_tutoria(self, prob_riesgo, nota_actual, asistencia):
        """
        Asigna nivel institucional y recomendación de acompañamiento pedagógico.
        """
        if prob_riesgo >= 0.65 or nota_actual < 6.0:
            nivel = "ALTO"
            color = "ROJO (CRÍTICO)"
            accion = "Tutoría Académica Obligatoria y Derivación a Bienestar Estudiantil"
            plan = "1. Sesión tutorial individual semanal. 2. Plan de refuerzo en temas críticos. 3. Monitoreo continuo de asistencia."
        elif prob_riesgo >= 0.35 or nota_actual < 7.0:
            nivel = "MEDIO"
            color = "AMARILLO (ADVERTENCIA)"
            accion = "Acompañamiento Tutorial Preventivo y Talleres de Estudio"
            plan = "1. Entrevista de seguimiento bimensual. 2. Talleres grupales de resolución de ejercicios."
        else:
            nivel = "BAJO"
            color = "VERDE (ÓPTIMO)"
            accion = "Seguimiento Regular de Aula"
            plan = "1. Continuar con el ritmo académico habitual. 2. Oportunidad de participación como mentor/ayudante."
            
        return nivel, color, accion, plan

    def evaluar_poblacion(self, df):
        print("  >> Evaluando población estudiantil en el Prototipo UNACH-LA...")
        X_eval = df.copy()
        leak_cols = ['nota_final', 'primer_parcial', 'segundo_parcial',
                     'nota_record', 'nota_trabajo', 'nota_sustentacion',
                     'promedio_grado', 'tiene_titulacion', 'estado_estudiante',
                     'modalidad_titulacion', 'num_matriculas_titulacion',
                     'id_estudiante', 'codigo_asignatura']
        
        for col in self.encoders:
            if col in X_eval.columns:
                le = self.encoders[col]
                X_eval[col] = X_eval[col].astype(str).map(
                    lambda s: le.transform([s])[0] if s in le.classes_ else 0
                )
                
        X_eval = X_eval.drop(columns=[c for c in leak_cols if c in X_eval.columns])
        X_eval = X_eval.fillna(X_eval.median())
        
        probs = self.modelo.predict_proba(X_eval)[:, 1]
        
        resultados = []
        for idx, row in df.iterrows():
            prob = float(probs[idx])
            nota = float(row.get('nota_final', 7.0))
            asist = float(row.get('porcentaje_asistencia', 85.0))
            nivel, color, accion, plan = self.generar_plan_tutoria(prob, nota, asist)
            
            resultados.append({
                'id_estudiante': str(row.get('id_estudiante', f'EST-{idx+1000}')),
                'carrera': str(row.get('carrera', 'Carrera General')),
                'semestre': str(row.get('semestre', 'Nivel General')),
                'nota_actual': round(nota, 2),
                'porcentaje_asistencia': round(asist, 2),
                'probabilidad_riesgo_ml': round(prob * 100, 2),
                'nivel_riesgo': nivel,
                'semaforo': color,
                'accion_recomendada': accion,
                'plan_acompanamiento': plan
            })
            
        df_resultados = pd.DataFrame(resultados)
        return df_resultados

def generar_manual_unach_la(df_eval):
    total = len(df_eval)
    alto = len(df_eval[df_eval['nivel_riesgo'] == 'ALTO'])
    medio = len(df_eval[df_eval['nivel_riesgo'] == 'MEDIO'])
    bajo = len(df_eval[df_eval['nivel_riesgo'] == 'BAJO'])
    
    md = f"""# Consolidación del Prototipo Funcional y Modelo UNACH-LA
## Universidad Nacional de Chimborazo - Sistema Institucional de Learning Analytics

**Versión del Prototipo**: 1.0 (Prototipo Funcional Completo)  
**Fecha de Consolidación**: {datetime.now().strftime('%Y-%m-%d')}  
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

El prototipo funcional se ejecutó sobre **{total:,} estudiantes**, obteniendo la siguiente distribución operativa de riesgo y priorización tutorial:

| Nivel de Riesgo | Semáforo | N° de Estudiantes | Porcentaje | Acción Institucional Recomendada |
|:---:|:---:|:---:|:---:|:---|
| **ALTO** | 🔴 **ROJO (CRÍTICO)** | **{alto:,}** | **{alto/total*100:.1f}%** | Tutoría académica obligatoria y derivación a Bienestar Estudiantil. |
| **MEDIO** | 🟡 **AMARILLO (ADVERTENCIA)** | **{medio:,}** | **{medio/total*100:.1f}%** | Acompañamiento preventivo y talleres de refuerzo. |
| **BAJO** | 🟢 **VERDE (ÓPTIMO)** | **{bajo:,}** | **{bajo/total*100:.1f}%** | Seguimiento regular en aula. |

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
"""
    with open(MANUAL_PATH, 'w', encoding='utf-8') as f:
        f.write(md)
    print(f"  >> Documento de Consolidación UNACH-LA generado en: {MANUAL_PATH}")

def main():
    print(f"\n{'='*70}\n  INICIANDO PROTOTIPO FUNCIONAL COMPLETO UNACH-LA\n{'='*70}")
    df = pd.read_csv(DATASET_PATH)
    
    motor = PrototipoUNACHLA()
    motor.entrenar_motor(df)
    
    df_eval = motor.evaluar_poblacion(df)
    
    # Exportar CSV
    df_eval.to_csv(EXPORT_CSV_PATH, index=False, encoding='utf-8-sig')
    print(f"  >> Archivo CSV con {len(df_eval)} evaluaciones guardado en: {EXPORT_CSV_PATH}")
    
    # Exportar JSON (casos críticos de prioridad ALTA y MEDIA)
    alertas_criticas = df_eval[df_eval['nivel_riesgo'].isin(['ALTO', 'MEDIO'])].head(100).to_dict(orient='records')
    resumen_json = {
        'fecha_ejecucion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_estudiantes_evaluados': len(df_eval),
        'resumen_riesgo': {
            'alto': int((df_eval['nivel_riesgo'] == 'ALTO').sum()),
            'medio': int((df_eval['nivel_riesgo'] == 'MEDIO').sum()),
            'bajo': int((df_eval['nivel_riesgo'] == 'BAJO').sum())
        },
        'top_alertas_prioritarias': alertas_criticas
    }
    with open(EXPORT_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(resumen_json, f, indent=2, ensure_ascii=False)
    print(f"  >> Alertas en JSON guardadas en: {EXPORT_JSON_PATH}")
    
    generar_manual_unach_la(df_eval)
    print(f"{'='*70}\n  PROTOTIPO FUNCIONAL UNACH-LA COMPLETADO CON ÉXITO\n{'='*70}\n")

if __name__ == '__main__':
    main()
