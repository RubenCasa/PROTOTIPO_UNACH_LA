import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import m2cgen as m2c
import os

def entrenar_y_exportar():
    print("Cargando dataset...")
    df = pd.read_csv('dataset_procesado.csv')
    
    print("Preparando variables...")
    features = ['asistencia', 'nota_final', 'total_eventos']
    for f in features:
        if f not in df.columns:
            df[f] = np.random.randint(0, 100, len(df)) if f != 'nota_final' else np.random.uniform(0, 10, len(df))
            
    df['asistencia'] = df['asistencia'].fillna(0)
    df['nota_final'] = df['nota_final'].fillna(0)
    df['total_eventos'] = df['total_eventos'].fillna(0)
    
    # Definir clase de riesgo (0: Alto, 1: Medio, 2: Bajo)
    def asignar_riesgo(row):
        if row['nota_final'] < 6 or row['asistencia'] < 70 or row['total_eventos'] < 10:
            return 0 # Alto
        elif row['nota_final'] < 7.5 or row['asistencia'] < 80:
            return 1 # Medio
        else:
            return 2 # Bajo
            
    df['Riesgo'] = df.apply(asignar_riesgo, axis=1)
    
    X = df[features]
    y = df['Riesgo']
    
    print("Entrenando Decision Tree...")
    model = DecisionTreeClassifier(max_depth=5, random_state=42)
    model.fit(X, y)
    
    print("Exportando a JavaScript con m2cgen...")
    code = m2c.export_to_javascript(model)
    
    # m2cgen exporta una funcion llamada 'score'. La renombraremos y adaptaremos para parsear la salida.
    js_code = f"""// AUTO-GENERATED ML MODEL
// Exported from Python scikit-learn using m2cgen

/**
 * Predice el nivel de riesgo en base a 3 features: [asistencia, nota_final, total_eventos]
 * Retorna: 0 (Alto Riesgo), 1 (Riesgo Medio), 2 (Riesgo Bajo)
 */
export function predictRisk(input) {{
{code}
  // m2cgen returns an array with scores for each class [score0, score1, score2]
  const scores = score(input);
  // Devuelve el indice del maximo score
  return scores.indexOf(Math.max(...scores));
}}
"""
    # Guardar en la carpeta del backend y tambien en src/utils del frontend
    with open('ml_model.js', 'w', encoding='utf-8') as f:
        f.write(js_code)
        
    frontend_path = '../06_Dashboard_React/src/utils/ml_model.js'
    os.makedirs(os.path.dirname(frontend_path), exist_ok=True)
    with open(frontend_path, 'w', encoding='utf-8') as f:
        f.write(js_code)
        
    print(f"Modelo exportado exitosamente a {frontend_path}")

if __name__ == '__main__':
    entrenar_y_exportar()
