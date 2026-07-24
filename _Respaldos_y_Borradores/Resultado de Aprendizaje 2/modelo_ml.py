# -*- coding: utf-8 -*-
"""
Resultado de Aprendizaje 2: Diseno de Modelos ML para Diagnostico Academico
===========================================================================
Pipeline completo: EDA -> Feature Selection -> Entrenamiento -> Evaluacion

Target: en_riesgo (1 = nota_final < 7, 0 = nota_final >= 7)
Modelos: Logistic Regression, Decision Tree, Random Forest, XGBoost, SVM
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Backend no-interactivo
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import io
import warnings
import json
from datetime import datetime

from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, confusion_matrix, classification_report
)

# Fix encoding para Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURACION
# ============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_FILE = os.path.join(BASE_DIR, "dataset_procesado.csv")
GRAFICOS_DIR = os.path.join(BASE_DIR, "graficos")
RESULTADOS_JSON = os.path.join(BASE_DIR, "resultados_ml.json")

os.makedirs(GRAFICOS_DIR, exist_ok=True)

# Configuracion global de matplotlib
plt.rcParams.update({
    'figure.figsize': (10, 6),
    'figure.dpi': 150,
    'font.size': 11,
    'font.family': 'sans-serif',
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.2,
})

SEED = 42
np.random.seed(SEED)

# Paleta de colores profesional
COLORS = {
    'primary': '#1F4E79',
    'secondary': '#2E75B6',
    'accent': '#BDD7EE',
    'danger': '#C00000',
    'success': '#548235',
    'warning': '#ED7D31',
    'bg': '#F2F7FB',
    'riesgo': '#E74C3C',
    'no_riesgo': '#2ECC71',
}

def print_section(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")

def print_step(step):
    print(f"  >> {step}")


# ============================================================================
# PASO 1: CARGAR DATOS Y DEFINIR TARGET
# ============================================================================
def paso1_definir_target():
    print_section("PASO 1: CARGAR DATOS Y DEFINIR TARGET")

    df = pd.read_csv(DATASET_FILE)
    print_step(f"Dataset cargado: {df.shape}")

    # Crear variable target
    df['en_riesgo'] = (df['nota_final'] < 7).astype(int)
    print_step(f"Target 'en_riesgo' creado:")
    print_step(f"  En riesgo (1): {df['en_riesgo'].sum()} ({df['en_riesgo'].mean()*100:.1f}%)")
    print_step(f"  Sin riesgo (0): {(df['en_riesgo']==0).sum()} ({(1-df['en_riesgo'].mean())*100:.1f}%)")

    # Eliminar columnas con data leakage
    leak_cols = ['nota_final', 'primer_parcial', 'segundo_parcial',
                 'nota_record', 'nota_trabajo', 'nota_sustentacion',
                 'promedio_grado', 'tiene_titulacion', 'estado_estudiante',
                 'modalidad_titulacion', 'num_matriculas_titulacion']
    
    leak_presentes = [c for c in leak_cols if c in df.columns]
    df = df.drop(columns=leak_presentes)
    print_step(f"Columnas con data leakage eliminadas ({len(leak_presentes)}): {leak_presentes}")

    # Eliminar ID (no es feature)
    if 'id_estudiante' in df.columns:
        df = df.drop(columns=['id_estudiante'])
    # Eliminar codigo_asignatura (demasiados valores unicos, no generaliza)
    if 'codigo_asignatura' in df.columns:
        df = df.drop(columns=['codigo_asignatura'])

    print_step(f"Shape final: {df.shape}")

    return df


# ============================================================================
# PASO 2: EDA CON VISUALIZACIONES
# ============================================================================
def paso2_eda(df):
    print_section("PASO 2: EDA - ANALISIS EXPLORATORIO")

    target = df['en_riesgo']
    features = df.drop(columns=['en_riesgo'])

    # --- 2.1 Distribucion del target ---
    print_step("Generando distribucion del target...")
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Pie chart
    valores = target.value_counts()
    labels = ['Sin Riesgo (nota >= 7)', 'En Riesgo (nota < 7)']
    colors_pie = [COLORS['no_riesgo'], COLORS['riesgo']]
    axes[0].pie(valores.values, labels=labels, colors=colors_pie,
                autopct='%1.1f%%', startangle=90, textprops={'fontsize': 12})
    axes[0].set_title('Distribucion de la Variable Target', fontweight='bold')

    # Bar chart
    bars = axes[1].bar(['Sin Riesgo\n(nota >= 7)', 'En Riesgo\n(nota < 7)'],
                       [valores[0], valores[1]], color=colors_pie, edgecolor='white', linewidth=2)
    axes[1].set_ylabel('Cantidad de Registros')
    axes[1].set_title('Balance de Clases', fontweight='bold')
    for bar, val in zip(bars, [valores[0], valores[1]]):
        axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30,
                     f'{val:,}', ha='center', fontweight='bold', fontsize=13)

    plt.tight_layout()
    plt.savefig(os.path.join(GRAFICOS_DIR, '01_distribucion_target.png'))
    plt.close()

    # --- 2.2 Correlacion features numericas ---
    print_step("Generando heatmap de correlacion...")
    num_cols = features.select_dtypes(include=[np.number]).columns.tolist()

    # Top correlaciones con el target
    correlaciones = df[num_cols + ['en_riesgo']].corr()['en_riesgo'].drop('en_riesgo')
    top_corr = correlaciones.abs().sort_values(ascending=False).head(20)

    fig, ax = plt.subplots(figsize=(10, 8))
    top_corr_cols = top_corr.index.tolist()
    corr_matrix = df[top_corr_cols].corr()
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r',
                center=0, square=True, linewidths=0.5, ax=ax,
                annot_kws={'size': 8})
    ax.set_title('Correlacion entre Top-20 Features (vs Target)', fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(GRAFICOS_DIR, '02_heatmap_correlacion.png'))
    plt.close()

    # --- 2.3 Correlacion con el target (barplot) ---
    print_step("Generando correlaciones con el target...")
    fig, ax = plt.subplots(figsize=(12, 8))
    top_25 = correlaciones.abs().sort_values(ascending=True).tail(25)
    colors_bar = [COLORS['danger'] if correlaciones[c] > 0 else COLORS['secondary']
                  for c in top_25.index]
    top_25_vals = [correlaciones[c] for c in top_25.index]
    ax.barh(range(len(top_25)), top_25_vals, color=colors_bar, edgecolor='white')
    ax.set_yticks(range(len(top_25)))
    ax.set_yticklabels(top_25.index, fontsize=9)
    ax.set_xlabel('Correlacion con en_riesgo')
    ax.set_title('Top-25 Correlaciones con la Variable Target', fontweight='bold')
    ax.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
    # Leyenda
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=COLORS['danger'], label='Correlacion positiva (+ riesgo)'),
                       Patch(facecolor=COLORS['secondary'], label='Correlacion negativa (- riesgo)')]
    ax.legend(handles=legend_elements, loc='lower right')
    plt.tight_layout()
    plt.savefig(os.path.join(GRAFICOS_DIR, '03_correlacion_target.png'))
    plt.close()

    # --- 2.4 Boxplots features clave por clase ---
    print_step("Generando boxplots por clase...")
    features_clave = ['asistencia', 'tutorias', 'puntaje_admision', 'promedio_nivelacion',
                      'total_eventos', 'calificacion_lms_promedio', 'dias_activos',
                      'tiempo_conexion_promedio_min']
    features_clave = [f for f in features_clave if f in df.columns]

    fig, axes = plt.subplots(2, 4, figsize=(18, 10))
    axes = axes.flatten()
    for i, feat in enumerate(features_clave[:8]):
        ax = axes[i]
        data_0 = df[df['en_riesgo'] == 0][feat].dropna()
        data_1 = df[df['en_riesgo'] == 1][feat].dropna()
        bp = ax.boxplot([data_0, data_1], labels=['Sin\nRiesgo', 'En\nRiesgo'],
                        patch_artist=True, widths=0.6)
        bp['boxes'][0].set_facecolor(COLORS['no_riesgo'])
        bp['boxes'][1].set_facecolor(COLORS['riesgo'])
        for box in bp['boxes']:
            box.set_alpha(0.7)
        ax.set_title(feat, fontweight='bold', fontsize=10)
        ax.grid(axis='y', alpha=0.3)
    for j in range(len(features_clave), len(axes)):
        axes[j].set_visible(False)
    fig.suptitle('Distribucion de Features Clave por Clase de Riesgo', fontweight='bold', fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(GRAFICOS_DIR, '04_boxplots_features.png'))
    plt.close()

    # --- 2.5 Variables categoricas vs target ---
    print_step("Generando analisis de categoricas...")
    cat_cols = ['genero', 'etnia', 'sector_procedencia', 'sector_residencia',
                'enfermedad', 'tipo_beca', 'dificultad_aprendizaje', 'nombre_asignatura']
    cat_cols = [c for c in cat_cols if c in df.columns]

    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    axes = axes.flatten()
    for i, col in enumerate(cat_cols[:8]):
        ax = axes[i]
        ct = pd.crosstab(df[col], df['en_riesgo'], normalize='index') * 100
        ct.columns = ['Sin Riesgo %', 'En Riesgo %']
        ct.plot(kind='bar', stacked=True, ax=ax,
                color=[COLORS['no_riesgo'], COLORS['riesgo']], alpha=0.8, edgecolor='white')
        ax.set_title(col, fontweight='bold', fontsize=10)
        ax.set_ylabel('Porcentaje')
        ax.set_xlabel('')
        ax.legend(fontsize=7, loc='upper right')
        ax.tick_params(axis='x', rotation=45, labelsize=8)
        ax.set_ylim(0, 110)
    for j in range(len(cat_cols), len(axes)):
        axes[j].set_visible(False)
    fig.suptitle('Variables Categoricas vs Riesgo Academico', fontweight='bold', fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(GRAFICOS_DIR, '05_categoricas_vs_target.png'))
    plt.close()

    print_step(f"Graficos EDA guardados en: {GRAFICOS_DIR}")
    return correlaciones


# ============================================================================
# PASO 3: PREPARACION PARA MODELADO
# ============================================================================
def paso3_preparar_datos(df):
    print_section("PASO 3: PREPARACION PARA MODELADO")

    y = df['en_riesgo']
    X = df.drop(columns=['en_riesgo'])

    # Identificar tipos
    cat_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()
    num_cols = X.select_dtypes(include=[np.number]).columns.tolist()
    print_step(f"Features numericas: {len(num_cols)}")
    print_step(f"Features categoricas: {len(cat_cols)}: {cat_cols}")

    # Encoding de categoricas
    label_encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        label_encoders[col] = le

    print_step(f"Label Encoding aplicado a {len(cat_cols)} columnas")

    # Tratar NaN restantes
    nan_count = X.isnull().sum().sum()
    if nan_count > 0:
        X = X.fillna(X.median())
        print_step(f"NaN imputados con mediana: {nan_count} valores")

    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=SEED, stratify=y
    )
    print_step(f"Train: {X_train.shape}, Test: {X_test.shape}")
    print_step(f"  Train target: {y_train.value_counts().to_dict()}")
    print_step(f"  Test target:  {y_test.value_counts().to_dict()}")

    # Escalado
    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(
        scaler.fit_transform(X_train),
        columns=X_train.columns, index=X_train.index
    )
    X_test_scaled = pd.DataFrame(
        scaler.transform(X_test),
        columns=X_test.columns, index=X_test.index
    )
    print_step("StandardScaler aplicado")

    return X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test, X.columns.tolist(), scaler


# ============================================================================
# PASO 4: SELECCION DE FEATURES
# ============================================================================
def paso4_seleccion_features(X_train, y_train, feature_names, correlaciones_target):
    print_section("PASO 4: SELECCION DE FEATURES")

    # Feature importance con Random Forest
    print_step("Calculando feature importance con Random Forest...")
    rf_selector = RandomForestClassifier(n_estimators=200, random_state=SEED, n_jobs=-1)
    rf_selector.fit(X_train, y_train)

    importances = pd.Series(rf_selector.feature_importances_, index=X_train.columns)
    importances = importances.sort_values(ascending=False)

    # Grafico de feature importance
    fig, ax = plt.subplots(figsize=(12, 10))
    top_30 = importances.head(30)
    bars = ax.barh(range(len(top_30)), top_30.values[::-1],
                   color=COLORS['secondary'], edgecolor='white', alpha=0.85)
    ax.set_yticks(range(len(top_30)))
    ax.set_yticklabels(top_30.index[::-1], fontsize=9)
    ax.set_xlabel('Importancia (Random Forest)')
    ax.set_title('Top-30 Features mas Importantes (Random Forest)', fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(GRAFICOS_DIR, '06_feature_importance.png'))
    plt.close()

    print_step(f"Top-10 features:")
    for i, (feat, imp) in enumerate(importances.head(10).items()):
        print(f"      {i+1}. {feat}: {imp:.4f}")

    return importances


# ============================================================================
# PASO 5: ENTRENAMIENTO DE MODELOS
# ============================================================================
def paso5_entrenar_modelos(X_train_scaled, X_train, y_train):
    print_section("PASO 5: ENTRENAMIENTO DE MODELOS")

    modelos = {
        'Logistic Regression': LogisticRegression(
            max_iter=1000, random_state=SEED, C=1.0
        ),
        'Decision Tree': DecisionTreeClassifier(
            max_depth=10, min_samples_split=10, random_state=SEED
        ),
        'Random Forest': RandomForestClassifier(
            n_estimators=200, max_depth=15, min_samples_split=5,
            random_state=SEED, n_jobs=-1
        ),
        'XGBoost': XGBClassifier(
            n_estimators=200, max_depth=6, learning_rate=0.1,
            random_state=SEED, eval_metric='logloss',
            use_label_encoder=False, verbosity=0
        ),
        'SVM': SVC(
            kernel='rbf', C=1.0, gamma='scale',
            probability=True, random_state=SEED
        ),
    }

    # Validacion cruzada
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)

    resultados_cv = {}
    modelos_entrenados = {}

    for nombre, modelo in modelos.items():
        print_step(f"Entrenando {nombre}...")

        # Usar datos escalados para LR y SVM, sin escalar para arboles
        if nombre in ['Logistic Regression', 'SVM']:
            X_fit = X_train_scaled
        else:
            X_fit = X_train

        # Cross-validation
        scores_acc = cross_val_score(modelo, X_fit, y_train, cv=cv, scoring='accuracy')
        scores_f1 = cross_val_score(modelo, X_fit, y_train, cv=cv, scoring='f1')
        scores_roc = cross_val_score(modelo, X_fit, y_train, cv=cv, scoring='roc_auc')

        resultados_cv[nombre] = {
            'accuracy_mean': scores_acc.mean(),
            'accuracy_std': scores_acc.std(),
            'f1_mean': scores_f1.mean(),
            'f1_std': scores_f1.std(),
            'roc_auc_mean': scores_roc.mean(),
            'roc_auc_std': scores_roc.std(),
        }

        print(f"      Accuracy: {scores_acc.mean():.4f} (+/- {scores_acc.std():.4f})")
        print(f"      F1-Score: {scores_f1.mean():.4f} (+/- {scores_f1.std():.4f})")
        print(f"      AUC-ROC:  {scores_roc.mean():.4f} (+/- {scores_roc.std():.4f})")

        # Entrenar modelo final
        modelo.fit(X_fit, y_train)
        modelos_entrenados[nombre] = modelo

    return modelos_entrenados, resultados_cv


# ============================================================================
# PASO 6: EVALUACION DE MODELOS
# ============================================================================
def paso6_evaluar_modelos(modelos_entrenados, X_test, X_test_scaled, y_test, resultados_cv):
    print_section("PASO 6: EVALUACION EN TEST SET")

    resultados_test = {}

    for nombre, modelo in modelos_entrenados.items():
        if nombre in ['Logistic Regression', 'SVM']:
            X_eval = X_test_scaled
        else:
            X_eval = X_test

        y_pred = modelo.predict(X_eval)
        y_prob = modelo.predict_proba(X_eval)[:, 1]

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_prob)
        cm = confusion_matrix(y_test, y_pred)

        resultados_test[nombre] = {
            'accuracy': acc,
            'precision': prec,
            'recall': rec,
            'f1': f1,
            'auc_roc': auc,
            'confusion_matrix': cm.tolist(),
            'y_prob': y_prob,
        }

        print_step(f"{nombre}:")
        print(f"      Accuracy:  {acc:.4f}")
        print(f"      Precision: {prec:.4f}")
        print(f"      Recall:    {rec:.4f}")
        print(f"      F1-Score:  {f1:.4f}")
        print(f"      AUC-ROC:   {auc:.4f}")

    # --- Grafico: Tabla comparativa ---
    print_step("Generando tabla comparativa...")
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.axis('off')

    cell_text = []
    model_names = list(resultados_test.keys())
    for nombre in model_names:
        r = resultados_test[nombre]
        cv = resultados_cv[nombre]
        cell_text.append([
            f"{r['accuracy']:.4f}",
            f"{r['precision']:.4f}",
            f"{r['recall']:.4f}",
            f"{r['f1']:.4f}",
            f"{r['auc_roc']:.4f}",
            f"{cv['accuracy_mean']:.4f} +/- {cv['accuracy_std']:.4f}",
        ])

    table = ax.table(
        cellText=cell_text,
        rowLabels=model_names,
        colLabels=['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC-ROC', 'CV Accuracy'],
        cellLoc='center', rowLoc='center', loc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.8)

    # Colorear header
    for j in range(6):
        table[(0, j)].set_facecolor(COLORS['primary'])
        table[(0, j)].set_text_props(color='white', fontweight='bold')
    for i in range(len(model_names)):
        table[(i+1, -1)].set_text_props(fontweight='bold')
    
    # Highlight mejor modelo
    best_model_idx = max(range(len(model_names)),
                        key=lambda i: resultados_test[model_names[i]]['f1'])
    for j in range(6):
        table[(best_model_idx+1, j)].set_facecolor('#D4EDDA')

    ax.set_title('Comparacion de Modelos de Clasificacion', fontweight='bold',
                 fontsize=14, pad=20)
    plt.savefig(os.path.join(GRAFICOS_DIR, '07_tabla_comparativa.png'))
    plt.close()

    # --- Grafico: Matrices de confusion ---
    print_step("Generando matrices de confusion...")
    fig, axes = plt.subplots(1, 5, figsize=(25, 5))
    for i, (nombre, r) in enumerate(resultados_test.items()):
        ax = axes[i]
        cm = np.array(r['confusion_matrix'])
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                    xticklabels=['Sin Riesgo', 'En Riesgo'],
                    yticklabels=['Sin Riesgo', 'En Riesgo'],
                    annot_kws={'size': 14})
        ax.set_title(nombre, fontweight='bold', fontsize=11)
        ax.set_ylabel('Real' if i == 0 else '')
        ax.set_xlabel('Predicho')
    fig.suptitle('Matrices de Confusion', fontweight='bold', fontsize=14, y=1.05)
    plt.tight_layout()
    plt.savefig(os.path.join(GRAFICOS_DIR, '08_matrices_confusion.png'))
    plt.close()

    # --- Grafico: Curvas ROC ---
    print_step("Generando curvas ROC...")
    fig, ax = plt.subplots(figsize=(10, 8))
    colors_roc = ['#1F4E79', '#2E75B6', '#548235', '#ED7D31', '#C00000']
    for i, (nombre, r) in enumerate(resultados_test.items()):
        fpr, tpr, _ = roc_curve(y_test, r['y_prob'])
        ax.plot(fpr, tpr, color=colors_roc[i], linewidth=2.5,
                label=f"{nombre} (AUC = {r['auc_roc']:.4f})")
    ax.plot([0, 1], [0, 1], 'k--', alpha=0.5, linewidth=1, label='Random (AUC = 0.5)')
    ax.set_xlabel('Tasa de Falsos Positivos (FPR)')
    ax.set_ylabel('Tasa de Verdaderos Positivos (TPR)')
    ax.set_title('Curvas ROC - Comparacion de Modelos', fontweight='bold')
    ax.legend(loc='lower right', fontsize=11)
    ax.grid(alpha=0.3)
    ax.set_xlim([-0.02, 1.02])
    ax.set_ylim([-0.02, 1.02])
    plt.tight_layout()
    plt.savefig(os.path.join(GRAFICOS_DIR, '09_curvas_roc.png'))
    plt.close()

    # --- Grafico: Barras metricas ---
    print_step("Generando comparacion de metricas...")
    fig, ax = plt.subplots(figsize=(14, 7))
    metricas = ['accuracy', 'precision', 'recall', 'f1', 'auc_roc']
    x = np.arange(len(model_names))
    width = 0.15
    colors_met = ['#1F4E79', '#2E75B6', '#548235', '#ED7D31', '#C00000']

    for i, metrica in enumerate(metricas):
        valores = [resultados_test[m][metrica] for m in model_names]
        bars = ax.bar(x + i * width, valores, width, label=metrica.replace('_', ' ').upper(),
                      color=colors_met[i], alpha=0.85, edgecolor='white')

    ax.set_xlabel('Modelo')
    ax.set_ylabel('Valor de la Metrica')
    ax.set_title('Comparacion de Metricas por Modelo', fontweight='bold')
    ax.set_xticks(x + width * 2)
    ax.set_xticklabels(model_names, fontsize=10)
    ax.legend(loc='lower right')
    ax.set_ylim(0, 1.1)
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(GRAFICOS_DIR, '10_comparacion_metricas.png'))
    plt.close()

    # Identificar mejor modelo
    best_model = max(resultados_test.keys(),
                     key=lambda m: resultados_test[m]['f1'])
    print_step(f"\nMEJOR MODELO (por F1-Score): {best_model}")
    print_step(f"  F1 = {resultados_test[best_model]['f1']:.4f}, AUC = {resultados_test[best_model]['auc_roc']:.4f}")

    return resultados_test, best_model


# ============================================================================
# PASO 7: INTERPRETABILIDAD
# ============================================================================
def paso7_interpretabilidad(modelos_entrenados, feature_names, best_model_name):
    print_section("PASO 7: INTERPRETABILIDAD DEL MEJOR MODELO")

    # Feature importance del mejor modelo (o Random Forest si no es tree-based)
    if best_model_name in ['Random Forest', 'XGBoost', 'Decision Tree']:
        modelo = modelos_entrenados[best_model_name]
        importances = pd.Series(modelo.feature_importances_, index=feature_names)
    else:
        # Usar Random Forest como proxy
        modelo = modelos_entrenados['Random Forest']
        importances = pd.Series(modelo.feature_importances_, index=feature_names)
        print_step(f"(Usando Random Forest como proxy para feature importance)")

    importances = importances.sort_values(ascending=False)

    # Grafico Top-15
    fig, ax = plt.subplots(figsize=(12, 8))
    top_15 = importances.head(15)
    bars = ax.barh(range(len(top_15)), top_15.values[::-1],
                   color=COLORS['primary'], edgecolor='white', alpha=0.85)
    ax.set_yticks(range(len(top_15)))
    ax.set_yticklabels(top_15.index[::-1], fontsize=11)
    ax.set_xlabel('Importancia')
    ax.set_title(f'Top-15 Variables Predictivas ({best_model_name})', fontweight='bold')
    ax.grid(axis='x', alpha=0.3)

    # Anotaciones de valor
    for i, (bar, val) in enumerate(zip(bars, top_15.values[::-1])):
        ax.text(bar.get_width() + 0.001, bar.get_y() + bar.get_height()/2,
                f'{val:.4f}', va='center', fontsize=9)

    plt.tight_layout()
    plt.savefig(os.path.join(GRAFICOS_DIR, '11_top15_interpretabilidad.png'))
    plt.close()

    print_step(f"Top-10 variables predictivas ({best_model_name}):")
    for i, (feat, imp) in enumerate(importances.head(10).items()):
        print(f"      {i+1}. {feat}: {imp:.4f}")

    return importances


# ============================================================================
# MAIN
# ============================================================================
def main():
    print_section("INICIO DEL PIPELINE ML - RESULTADO DE APRENDIZAJE 2")
    print(f"  Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Paso 1
    df = paso1_definir_target()

    # Paso 2
    correlaciones = paso2_eda(df)

    # Paso 3
    X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test, feature_names, scaler = paso3_preparar_datos(df)

    # Paso 4
    importances_rf = paso4_seleccion_features(X_train, y_train, feature_names, correlaciones)

    # Paso 5
    modelos_entrenados, resultados_cv = paso5_entrenar_modelos(X_train_scaled, X_train, y_train)

    # Paso 6
    resultados_test, best_model = paso6_evaluar_modelos(
        modelos_entrenados, X_test, X_test_scaled, y_test, resultados_cv
    )

    # Paso 7
    importances_final = paso7_interpretabilidad(modelos_entrenados, feature_names, best_model)

    # Guardar resultados para el generador de Word
    resultados_export = {
        'best_model': best_model,
        'feature_names': feature_names,
        'resultados_cv': resultados_cv,
        'resultados_test': {k: {kk: vv for kk, vv in v.items() if kk != 'y_prob'}
                            for k, v in resultados_test.items()},
        'top_features': importances_final.head(15).to_dict(),
        'target_distribution': {
            'en_riesgo': int((df['en_riesgo'] == 1).sum()),
            'sin_riesgo': int((df['en_riesgo'] == 0).sum()),
        },
        'dataset_shape': list(df.shape),
        'n_features': len(feature_names),
        'train_size': len(X_train),
        'test_size': len(X_test),
    }
    with open(RESULTADOS_JSON, 'w', encoding='utf-8') as f:
        json.dump(resultados_export, f, indent=2, ensure_ascii=False, default=str)

    print_step(f"\nResultados guardados: {RESULTADOS_JSON}")

    print_section("PIPELINE ML COMPLETADO")
    print_step(f"Mejor modelo: {best_model}")
    print_step(f"Graficos generados: {len(os.listdir(GRAFICOS_DIR))} archivos en {GRAFICOS_DIR}")
    print(f"\n{'='*70}\n  FIN\n{'='*70}\n")


if __name__ == '__main__':
    main()
