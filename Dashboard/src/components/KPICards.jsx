import React from 'react';
import { AlertTriangle, TrendingUp, Users, CheckCircle, Target } from 'lucide-react';

const iconMap = {
  KPI_01_Tasa_Riesgo_Academico: <AlertTriangle size={24} color="var(--status-warning)" />,
  KPI_02_Promedio_General_Notas: <TrendingUp size={24} color="var(--accent-color)" />,
  KPI_03_Asistencia_Promedio: <Users size={24} color="var(--status-optimal)" />,
  KPI_04_Efectividad_Modelo_ML: <Target size={24} color="#c084fc" />
};

export default function KPICards({ data }) {
  if (!data) return null;

  return (
    <div className="kpi-grid">
      {Object.entries(data).map(([key, kpi]) => (
        <div key={key} className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>{kpi.nombre}</span>
            {iconMap[key] || <CheckCircle size={24} />}
          </div>
          
          <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.5rem', margin: '0.5rem 0' }}>
            <span style={{ fontSize: '2rem', fontWeight: 'bold' }}>{kpi.valor}</span>
            <span style={{ fontSize: '1rem', color: 'var(--text-secondary)' }}>{kpi.unidad}</span>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem' }}>
            <span style={{ color: 'var(--text-secondary)' }}>Meta: {kpi.meta_institucional}</span>
            <span style={{ 
              fontWeight: '600',
              color: kpi.estado === 'CRÍTICO' ? 'var(--status-critical)' : 
                     kpi.estado === 'ADVERTENCIA' ? 'var(--status-warning)' : 'var(--status-optimal)'
            }}>
              {kpi.estado}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}
