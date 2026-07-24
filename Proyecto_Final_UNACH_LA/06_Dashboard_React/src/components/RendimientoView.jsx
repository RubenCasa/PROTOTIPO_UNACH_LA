import React from 'react';
import KPIGrid from './KPIGrid';
import { TrendingUp } from 'lucide-react';

export default function RendimientoView({ kpis }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      <div className="header">
        <div>
          <h1 style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <TrendingUp color="var(--status-yellow)" />
            Rendimiento Académico
          </h1>
          <p>Análisis de métricas institucionales y comportamiento del estudiante.</p>
        </div>
      </div>
      
      <KPIGrid data={kpis} />
      
      <div className="glass-panel" style={{ minHeight: '300px', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <p style={{ color: 'var(--text-muted)' }}>Módulo de visualización avanzada en desarrollo. (Gráficas de Series Temporales SICOA)</p>
      </div>
    </div>
  );
}
