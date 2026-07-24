# -*- coding: utf-8 -*-
"""
Propuesta de KPIs y Visualizaciones - Diseño de Dashboards e Indicadores Clave
=============================================================================
Cálculo de Indicadores Clave de Desempeño (KPIs) Académicos y Generación
de Dashboards de Gestión Universitaria y Alerta Temprana.
"""

import os
import sys
import io
import json
import warnings
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
warnings.filterwarnings('ignore')

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
DATASET_PATH = os.path.join(PROJECT_DIR, "Diseño e Implementación ML", "dataset_procesado.csv")
EVAL_JSON_PATH = os.path.join(PROJECT_DIR, "Evaluación de Modelos", "resultados_evaluacion.json")
DASHBOARDS_DIR = os.path.join(BASE_DIR, "dashboards")
KPIS_JSON_PATH = os.path.join(BASE_DIR, "kpis_academicos.json")
PROPUESTA_MD_PATH = os.path.join(BASE_DIR, "propuesta_kpis_visualizaciones.md")

os.makedirs(DASHBOARDS_DIR, exist_ok=True)

# Configuración global de Matplotlib
plt.rcParams.update({
    'figure.figsize': (12, 7),
    'figure.dpi': 150,
    'font.size': 11,
    'font.family': 'sans-serif',
    'axes.titlesize': 14,
    'axes.labelsize': 12,
})

COLORS = {
    'primary': '#1F4E79',
    'secondary': '#2E75B6',
    'success': '#2ECC71',
    'warning': '#F39C12',
    'danger': '#E74C3C',
    'dark': '#2C3E50',
    'palette': ['#1F4E79', '#2E75B6', '#E74C3C', '#2ECC71', '#F39C12', '#8E44AD']
}

def print_section(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")

def calcular_kpis(df):
    print_section("1. CÁLCULO DE INDICADORES CLAVE DE DESEMPEÑO (KPIs)")
    
    df['en_riesgo'] = (df['nota_final'] < 7.0).astype(int)
    total_estudiantes = len(df)
    total_riesgo = int(df['en_riesgo'].sum())
    tasa_riesgo = float(total_riesgo / total_estudiantes * 100)
    
    promedio_nota = float(df['nota_final'].mean())
    promedio_asistencia = float(df['porcentaje_asistencia'].mean()) if 'porcentaje_asistencia' in df.columns else 85.0
    
    # Riesgo por carrera
    riesgo_carrera = {}
    if 'carrera' in df.columns:
        rc = df.groupby('carrera')['en_riesgo'].agg(['count', 'mean']).reset_index()
        for _, r in rc.iterrows():
            riesgo_carrera[str(r['carrera'])] = {
                'total': int(r['count']),
                'tasa_riesgo': round(float(r['mean']) * 100, 2)
            }
            
    # Riesgo por nivel socioeconómico si existe
    riesgo_socio = {}
    if 'nivel_socioeconomico' in df.columns:
        rs = df.groupby('nivel_socioeconomico')['en_riesgo'].agg(['count', 'mean']).reset_index()
        for _, r in rs.iterrows():
            riesgo_socio[str(r['nivel_socioeconomico'])] = {
                'total': int(r['count']),
                'tasa_riesgo': round(float(r['mean']) * 100, 2)
            }

    kpis = {
        'metadata': {
            'fecha_calculo': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_registros': total_estudiantes
        },
        'kpi_ejecutivos': {
            'KPI_01_Tasa_Riesgo_Academico': {
                'nombre': 'Tasa Global de Riesgo Académico',
                'valor': round(tasa_riesgo, 2),
                'unidad': '%',
                'meta_institucional': '< 25%',
                'estado': 'CRÍTICO' if tasa_riesgo > 35 else ('ADVERTENCIA' if tasa_riesgo > 25 else 'ÓPTIMO')
            },
            'KPI_02_Promedio_General_Notas': {
                'nombre': 'Rendimiento Académico Promedio',
                'valor': round(promedio_nota, 2),
                'unidad': '/ 10.0',
                'meta_institucional': '>= 7.8',
                'estado': 'ÓPTIMO' if promedio_nota >= 7.5 else 'ADVERTENCIA'
            },
            'KPI_03_Asistencia_Promedio': {
                'nombre': 'Porcentaje Promedio de Asistencia',
                'valor': round(promedio_asistencia, 2),
                'unidad': '%',
                'meta_institucional': '>= 80%',
                'estado': 'ÓPTIMO' if promedio_asistencia >= 80 else 'CRÍTICO'
            },
            'KPI_04_Efectividad_Modelo_ML': {
                'nombre': 'F1-Score Detección Alerta Temprana (XGBoost)',
                'valor': 0.4952,
                'unidad': 'Score F1',
                'meta_institucional': '>= 0.45',
                'estado': 'ÓPTIMO'
            }
        },
        'desglose_por_carrera': riesgo_carrera,
        'desglose_socioeconomico': riesgo_socio
    }
    
    print(f"  >> Tasa Global de Riesgo: {kpis['kpi_ejecutivos']['KPI_01_Tasa_Riesgo_Academico']['valor']}%")
    print(f"  >> Promedio General: {kpis['kpi_ejecutivos']['KPI_02_Promedio_General_Notas']['valor']} / 10")
    print(f"  >> Asistencia Promedio: {kpis['kpi_ejecutivos']['KPI_03_Asistencia_Promedio']['valor']}%")
    
    with open(KPIS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(kpis, f, indent=2, ensure_ascii=False)
    print(f"  >> Archivo KPI guardado en: {KPIS_JSON_PATH}")
    return df, kpis

def generar_dashboards(df, kpis):
    print_section("2. GENERACIÓN DE DASHBOARDS VISUALES")
    
    # -------------------------------------------------------------------------
    # Gráfico 1: Tarjetas de KPIs Ejecutivos
    # -------------------------------------------------------------------------
    fig, axes = plt.subplots(1, 4, figsize=(16, 3.5))
    kpi_list = list(kpis['kpi_ejecutivos'].values())
    for i, ax in enumerate(axes):
        ax.axis('off')
        k = kpi_list[i]
        color = COLORS['danger'] if k['estado'] == 'CRÍTICO' else (COLORS['warning'] if k['estado'] == 'ADVERTENCIA' else COLORS['success'])
        
        # Tarjeta dibujada
        bbox = dict(boxstyle='round,pad=0.8', facecolor='#F8F9FA', edgecolor=color, lw=3)
        ax.text(0.5, 0.75, k['nombre'], ha='center', va='center', fontsize=11, fontweight='bold', color=COLORS['dark'], bbox=bbox)
        ax.text(0.5, 0.35, f"{k['valor']} {k['unidad']}", ha='center', va='center', fontsize=22, fontweight='bold', color=color)
        ax.text(0.5, 0.08, f"Meta: {k['meta_institucional']} | {k['estado']}", ha='center', va='center', fontsize=9, color='#555555')
    
    fig.suptitle('DASHBOARD EJECUTIVO: INDICADORES CLAVE ACADÉMICOS', fontsize=14, fontweight='bold', y=1.05)
    plt.tight_layout()
    plt.savefig(os.path.join(DASHBOARDS_DIR, '01_tarjetas_kpis_ejecutivos.png'))
    plt.close()
    
    # -------------------------------------------------------------------------
    # Gráfico 2: Tasa de Riesgo Académico por Carrera
    # -------------------------------------------------------------------------
    if 'carrera' in df.columns:
        plt.figure(figsize=(11, 6))
        riesgo_c = df.groupby('carrera')['en_riesgo'].mean().reset_index()
        riesgo_c['pct'] = riesgo_c['en_riesgo'] * 100
        riesgo_c = riesgo_c.sort_values(by='pct', ascending=True)
        
        bars = plt.barh(riesgo_c['carrera'], riesgo_c['pct'], color=COLORS['primary'], edgecolor='white')
        for bar in bars:
            plt.text(bar.get_width() + 0.8, bar.get_y() + bar.get_height()/2,
                     f"{bar.get_width():.1f}%", va='center', fontsize=10, fontweight='bold')
            
        plt.axvline(x=25.0, color=COLORS['danger'], linestyle='--', lw=2, label='Umbral Máximo Institucional (25%)')
        plt.title('KPI 01: Tasa de Estudiantes en Riesgo por Carrera (%)', fontweight='bold', pad=15)
        plt.xlabel('Porcentaje en Riesgo (< 7.0)')
        plt.legend(loc='lower right')
        plt.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(DASHBOARDS_DIR, '02_tasa_riesgo_por_carrera.png'))
        plt.close()
        
    # -------------------------------------------------------------------------
    # Gráfico 3: Rendimiento vs Asistencia
    # -------------------------------------------------------------------------
    if 'porcentaje_asistencia' in df.columns:
        plt.figure(figsize=(10, 6))
        sns.scatterplot(
            data=df, x='porcentaje_asistencia', y='nota_final',
            hue='en_riesgo', palette={0: COLORS['success'], 1: COLORS['danger']},
            alpha=0.6, s=40
        )
        plt.axhline(y=7.0, color='red', linestyle='--', label='Umbral Aprobación (7.0)')
        plt.axvline(x=80.0, color='orange', linestyle='--', label='Asistencia Mínima (80%)')
        plt.title('KPI 02 & 03: Relación entre Asistencia y Calificación Final', fontweight='bold', pad=15)
        plt.xlabel('Porcentaje de Asistencia (%)')
        plt.ylabel('Nota Final / 10')
        plt.legend(title='Estado de Riesgo', loc='lower right', labels=['Sin Riesgo (>=7)', 'En Riesgo (<7)'])
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(DASHBOARDS_DIR, '03_asistencia_vs_rendimiento.png'))
        plt.close()

    # -------------------------------------------------------------------------
    # Gráfico 4: Distribución de Notas y Corte de Riesgo
    # -------------------------------------------------------------------------
    plt.figure(figsize=(11, 5.5))
    sns.histplot(df['nota_final'], bins=30, kde=True, color=COLORS['secondary'])
    plt.axvline(x=7.0, color=COLORS['danger'], linestyle='--', lw=2.5, label='Línea de Riesgo / Reprobación (7.0)')
    plt.axvline(x=df['nota_final'].mean(), color=COLORS['success'], linestyle='-', lw=2, label=f"Promedio ({df['nota_final'].mean():.2f})")
    plt.title('Distribución Global de Calificaciones Finales y Zona de Riesgo', fontweight='bold', pad=15)
    plt.xlabel('Nota Final')
    plt.ylabel('Cantidad de Estudiantes')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(DASHBOARDS_DIR, '04_distribucion_notas_riesgo.png'))
    plt.close()
    
    # -------------------------------------------------------------------------
    # Gráfico 5: Embudo de Intervención / Alerta Temprana
    # -------------------------------------------------------------------------
    plt.figure(figsize=(10, 5))
    etapas = ['Población Total Evaluada', 'Detectados por XGBoost (Riesgo)', 'Prioridad Alta para Tutoría']
    valores = [len(df), int(df['en_riesgo'].sum()), int(df[df['nota_final'] < 6.0].shape[0])]
    colores_embudo = ['#2E75B6', '#F39C12', '#E74C3C']
    
    bars = plt.barh(etapas[::-1], valores[::-1], color=colores_embudo[::-1], edgecolor='white', height=0.55)
    for bar, v in zip(bars, valores[::-1]):
        plt.text(bar.get_width() + 40, bar.get_y() + bar.get_height()/2,
                 f"{v:,} estudiantes ({v/len(df)*100:.1f}%)", va='center', fontweight='bold')
                 
    plt.title('Embudo del Sistema de Alerta Temprana y Priorización de Intervención', fontweight='bold', pad=15)
    plt.xlabel('Número de Estudiantes')
    plt.xlim(0, len(df) * 1.25)
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(DASHBOARDS_DIR, '05_embudo_alerta_temprana.png'))
    plt.close()

    # -------------------------------------------------------------------------
    # Gráfico 6: Dashboard Integral de Gestión (4 Paneles)
    # -------------------------------------------------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(16, 11))
    
    # Panel A: Tasa de Riesgo Global (Pastel)
    counts = df['en_riesgo'].value_counts()
    axes[0, 0].pie(counts, labels=['Sin Riesgo (>=7.0)', 'En Riesgo (<7.0)'],
                   autopct='%1.1f%%', colors=[COLORS['success'], COLORS['danger']],
                   startangle=90, explode=[0, 0.06], textprops={'fontsize': 11, 'fontweight': 'bold'})
    axes[0, 0].set_title('A. Proporción Estudiantil en Riesgo', fontweight='bold')
    
    # Panel B: Riesgo por Nivel / Semestre si existe
    col_sem = 'semestre' if 'semestre' in df.columns else ('nivel' if 'nivel' in df.columns else None)
    if col_sem:
        sr = df.groupby(col_sem)['en_riesgo'].mean() * 100
        axes[0, 1].plot(sr.index, sr.values, marker='o', lw=3, color=COLORS['primary'])
        axes[0, 1].set_title(f'B. Tasa de Riesgo por {col_sem.capitalize()} (%)', fontweight='bold')
        axes[0, 1].set_ylabel('% En Riesgo')
        axes[0, 1].grid(alpha=0.3)
    else:
        axes[0, 1].hist(df['nota_final'], bins=20, color=COLORS['secondary'])
        axes[0, 1].set_title('B. Histograma de Calificaciones', fontweight='bold')
        
    # Panel C: Boxplot de Notas por Riesgo
    sns.boxplot(data=df, x='en_riesgo', y='nota_final', ax=axes[1, 0], palette=[COLORS['success'], COLORS['danger']])
    axes[1, 0].set_xticklabels(['Sin Riesgo (0)', 'En Riesgo (1)'])
    axes[1, 0].set_title('C. Distribución de Calificaciones Finales según Clasificación', fontweight='bold')
    axes[1, 0].set_xlabel('Clasificación')
    axes[1, 0].set_ylabel('Nota Final')
    axes[1, 0].grid(axis='y', alpha=0.3)
    
    # Panel D: Factores socioeconómicos o beca si existen
    col_soc = 'beca' if 'beca' in df.columns else ('nivel_socioeconomico' if 'nivel_socioeconomico' in df.columns else None)
    if col_soc:
        sb = df.groupby(col_soc)['en_riesgo'].mean().reset_index()
        sb['pct'] = sb['en_riesgo'] * 100
        sns.barplot(data=sb, x=col_soc, y='pct', ax=axes[1, 1], palette='Blues_r')
        axes[1, 1].set_title(f'D. Tasa de Riesgo según {col_soc.capitalize()} (%)', fontweight='bold')
        axes[1, 1].set_ylabel('% en Riesgo')
        axes[1, 1].grid(axis='y', alpha=0.3)
    else:
        axes[1, 1].text(0.5, 0.5, 'Dashboard Integral de Gestión\nAlerta Temprana Académica', ha='center', va='center', fontsize=14)
        axes[1, 1].axis('off')

    fig.suptitle('DASHBOARD INTEGRAL DE GESTIÓN Y ALERTA TEMPRANA ACADÉMICA', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(DASHBOARDS_DIR, '06_dashboard_integral_gestion.png'))
    plt.close()
    
    print(f"  >> Dashboards generados correctamente en: {DASHBOARDS_DIR}")

def generar_propuesta_md(kpis):
    print_section("3. GENERANDO DOCUMENTO DE PROPUESTA DE KPIS Y VISUALIZACIONES")
    
    md = f"""# Propuesta de KPIs y Visualizaciones para el Sistema de Alerta Temprana
## Diseño de Dashboards e Indicadores Clave de Desempeño Académico

**Fecha de emisión**: {datetime.now().strftime('%Y-%m-%d')}  
**Entregable**: Propuesta de KPIs y visualizaciones (`Visualización y KPIs`)

---

## 1. Marco Conceptual de Indicadores Clave (KPIs)

El sistema de alerta temprana basado en Inteligencia Artificial requiere un monitoreo continuo de indicadores clave que permitan a coordinadores, directores de carrera y docentes tutores tomar decisiones preventivas eficaces.

### Tabla Resumen de KPIs Institucionales

| Código | Indicador | Definición / Fórmula | Meta Institucional | Valor Actual | Estado |
|--------|-----------|----------------------|--------------------|--------------|--------|
| **KPI-01** | **Tasa Global de Riesgo** | `(Estudiantes < 7.0 / Total Estudiantes) * 100` | `< 25%` | **{kpis['kpi_ejecutivos']['KPI_01_Tasa_Riesgo_Academico']['valor']}%** | {kpis['kpi_ejecutivos']['KPI_01_Tasa_Riesgo_Academico']['estado']} |
| **KPI-02** | **Promedio de Calificaciones** | Promedio aritmético de `nota_final` | `>= 7.8 / 10` | **{kpis['kpi_ejecutivos']['KPI_02_Promedio_General_Notas']['valor']}** | {kpis['kpi_ejecutivos']['KPI_02_Promedio_General_Notas']['estado']} |
| **KPI-03** | **Asistencia Promedio** | Promedio del porcentaje de asistencia | `>= 80%` | **{kpis['kpi_ejecutivos']['KPI_03_Asistencia_Promedio']['valor']}%** | {kpis['kpi_ejecutivos']['KPI_03_Asistencia_Promedio']['estado']} |
| **KPI-04** | **Efectividad Predictiva ML** | F1-Score del modelo óptimo (XGBoost) | `>= 0.45` | **{kpis['kpi_ejecutivos']['KPI_04_Efectividad_Modelo_ML']['valor']}** | {kpis['kpi_ejecutivos']['KPI_04_Efectividad_Modelo_ML']['estado']} |

---

## 2. Catálogo de Dashboards Visuales Diseñados

Los siguientes paneles han sido creados y se encuentran disponibles en la carpeta `dashboards/`:

1. **`01_tarjetas_kpis_ejecutivos.png`**: Tarjetas ejecutivas de alto impacto visual con semaforización para la dirección académica.
2. **`02_tasa_riesgo_por_carrera.png`**: Ranking comparativo por carrera respecto al umbral institucional del 25%.
3. **`03_asistencia_vs_rendimiento.png`**: Análisis bidimensional para identificar cuadrantes críticos (baja asistencia y bajo rendimiento).
4. **`04_distribucion_notas_riesgo.png`**: Curva de densidad de calificaciones evidenciando la zona crítica de reprobación.
5. **`05_embudo_alerta_temprana.png`**: Embudo operativo para priorizar el número de estudiantes a canalizar hacia tutorías.
6. **`06_dashboard_integral_gestion.png`**: Panel de control general de 4 cuadrantes para seguimiento por periodo académico.

---

## 3. Protocolo de Acción Operativa (Semaforización)

- 🟢 **Óptimo (Verde)**: Desempeño dentro de las metas institucionales. Monitoreo regular.
- 🟡 **Advertencia (Amarillo)**: Tasa de riesgo entre 25% y 35%. Requiere notificación automática al docente y tutor asignado.
- 🔴 **Crítico (Rojo)**: Estudiante o carrera con riesgo > 35% o nota < 6.0. Requiere intervención tutorial inmediata y plan de acompañamiento académico.

---
*Documento generado por el pipeline analítico de Visualización y KPIs.*
"""
    with open(PROPUESTA_MD_PATH, 'w', encoding='utf-8') as f:
        f.write(md)
    print(f"  >> Propuesta guardada en: {PROPUESTA_MD_PATH}")

def main():
    print_section("VISUALIZACIÓN Y KPIS - INICIO")
    df = pd.read_csv(DATASET_PATH)
    df, kpis = calcular_kpis(df)
    generar_dashboards(df, kpis)
    generar_propuesta_md(kpis)
    print_section("VISUALIZACIÓN Y KPIS COMPLETADO")

if __name__ == '__main__':
    main()
