import React from 'react';
import KPIGrid from './KPIGrid';
import PredictionChart from './PredictionChart';
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
      
      {/* Gráfica de Proyección Lineal */}
      <PredictionChart />
      
    </div>
  );
}
