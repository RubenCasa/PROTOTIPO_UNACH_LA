# -*- coding: utf-8 -*-
import pandas as pd
import os
import gc

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_MATRICULADOS = os.path.join(BASE_DIR, "proyecto ML matriculados CD 2025 2S.xlsx")
FILE_ANONIMIZADOS = os.path.join(BASE_DIR, "Registros_usuarios_anonimizados_final.xlsx")
FILE_LMS = os.path.join(BASE_DIR, "dataset_LMS_2025_2S.xlsx")

OUTPUT_SICOA = os.path.join(BASE_DIR, "SICOA_Anonimizado_Listo.csv")
OUTPUT_MOODLE = os.path.join(BASE_DIR, "Moodle_Anonimizado_Listo.csv")

def preparar_datos_sicoa():
    print("Iniciando preparación de SICOA (Matriculados)...")
    if not os.path.exists(FILE_MATRICULADOS):
        print(f"Error: No se encuentra el archivo {FILE_MATRICULADOS}")
        return
        
    df_sicoa = pd.read_excel(FILE_MATRICULADOS)
    print(f"Dataset original cargado: {df_sicoa.shape}")
    
    # Estandarizar nombres de columnas a formato limpio si es necesario
    # Renombrar IdEstudianteAnonimo a un formato estandar para el dashboard
    if 'IdEstudianteAnonimo' in df_sicoa.columns:
        df_sicoa = df_sicoa.rename(columns={'IdEstudianteAnonimo': 'ID_Estudiante'})
    
    # Manejar nulos en promedios o notas
    cols_numericas = ['TotalPorcentajeAsistencia', 'PrimerParcial', 'SegundoParcial', 'EvaluacionSupletorio', 'PromedioFinalNumero']
    for col in cols_numericas:
        if col in df_sicoa.columns:
            df_sicoa[col] = pd.to_numeric(df_sicoa[col], errors='coerce').fillna(0)
    
    # Exportar a CSV para que el dashboard lo lea rapidamente sin problemas de memoria
    df_sicoa.to_csv(OUTPUT_SICOA, index=False, encoding='utf-8')
    print(f"Archivo estandarizado guardado en: {OUTPUT_SICOA}")

def aplicar_diccionario_anonimizacion(archivo_entrada, archivo_salida, columna_id_original):
    """
    Toma un archivo de datos (ej. logs LMS brutos), lee el gran diccionario de 140MB y 
    cruza los datos para generar un archivo anonimizado sin colgar la RAM (usando chunks o merges eficientes).
    """
    print(f"Aplicando diccionario de anonimización a {archivo_entrada}...")
    if not os.path.exists(FILE_ANONIMIZADOS):
        print(f"Error: No se encuentra el diccionario {FILE_ANONIMIZADOS}")
        return
        
    if not os.path.exists(archivo_entrada):
        print(f"Error: No se encuentra {archivo_entrada}")
        return

    # Leer el dataset objetivo
    if archivo_entrada.endswith('.csv'):
        df_target = pd.read_csv(archivo_entrada)
    else:
        df_target = pd.read_excel(archivo_entrada)
        
    if columna_id_original not in df_target.columns:
        print(f"Error: La columna {columna_id_original} no existe en el archivo destino.")
        return

    # Leer el diccionario pesado. Especificamos las columnas para ahorrar memoria.
    print("Cargando diccionario masivo (esto puede tomar un minuto)...")
    # Hay que usar el nombre correcto de la columna. El script anterior mostró "Cdigo aplicado".
    # Usaremos indexación posicional o el nombre exacto extraido
    columnas_diccionario = pd.read_excel(FILE_ANONIMIZADOS, nrows=0).columns.tolist()
    col_id_original = columnas_diccionario[0]  # 'ID original'
    col_codigo = columnas_diccionario[1]       # 'Código aplicado' (con posible error de codificación)
    
    df_dict = pd.read_excel(FILE_ANONIMIZADOS, usecols=[col_id_original, col_codigo])
    df_dict = df_dict.rename(columns={col_id_original: columna_id_original, col_codigo: 'ID_Estudiante'})

    # Cruzar datos (Left Join)
    print("Cruzando datos con el diccionario...")
    df_anon = df_target.merge(df_dict, on=columna_id_original, how='left')
    
    # Eliminar columna original por seguridad
    df_anon = df_anon.drop(columns=[columna_id_original])
    
    # Liberar memoria del diccionario
    del df_dict
    gc.collect()
    
    # Exportar
    df_anon.to_csv(archivo_salida, index=False, encoding='utf-8')
    print(f"Archivo anonimizado exportado a: {archivo_salida}")

def preparar_datos_moodle():
    print("\nIniciando preparación de Moodle (LMS)...")
    if not os.path.exists(FILE_LMS):
        print(f"Error: No se encuentra el archivo {FILE_LMS}")
        return
        
    print("Cargando archivo Excel de Moodle (esto puede tomar unos segundos)...")
    df_lms = pd.read_excel(FILE_LMS)
    print(f"Dataset Moodle cargado: {df_lms.shape}")
    
    # Exportar a CSV para lectura ultrarrápida en el Dashboard
    df_lms.to_csv(OUTPUT_MOODLE, index=False, encoding='utf-8')
    print(f"Archivo estandarizado guardado en: {OUTPUT_MOODLE}")

if __name__ == '__main__':
    preparar_datos_sicoa()
    preparar_datos_moodle()
    print("\n[Opcional] Ejemplo de uso de anonimizador profundo:")
    print("aplicar_diccionario_anonimizacion('logs_moodle_crudos.csv', 'Moodle_Anonimizado_Listo.csv', 'id_usuario')")
