import React from 'react';

export default function KPIGrid({ data }) {
  const kpis = [
    {
      key: 'KPI_01_Tasa_Riesgo_Academico',
      icon: '📉',
    },
    {
      key: 'KPI_02_Promedio_General_Notas',
      icon: '📈',
    },
    {
      key: 'KPI_03_Asistencia_Promedio',
      icon: '👥',
    },
    {
      key: 'KPI_04_Efectividad_Modelo_ML',
      icon: '🤖',
    }
  ];

  return (
    <div className="kpi-grid">
      {kpis.map((item, index) => {
        const kpi = data[item.key];
        if (!kpi) return null;
        
        let statusClass = 'badge-green';
        if (kpi.estado === 'CRÍTICO') statusClass = 'badge-red';
        if (kpi.estado === 'ADVERTENCIA') statusClass = 'badge-yellow';

        return (
          <div key={index} className="glass-panel kpi-card">
            <div className="kpi-header">
              <span>{kpi.nombre}</span>
              <span style={{ fontSize: '1.2rem' }}>{item.icon}</span>
            </div>
            <div className="kpi-value">
              {kpi.valor} <span className="kpi-unit">{kpi.unidad}</span>
            </div>
            <div className="kpi-footer">
              <span>Meta: {kpi.meta_institucional}</span>
              <span className={`badge ${statusClass}`}>{kpi.estado}</span>
            </div>
          </div>
        );
      })}
    </div>
  );
}
