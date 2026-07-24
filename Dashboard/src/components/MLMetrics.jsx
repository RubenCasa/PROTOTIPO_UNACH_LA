import React from 'react';
import { Brain, Award, Zap } from 'lucide-react';
import { ResponsiveContainer, Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Tooltip } from 'recharts';

export default function MLMetrics({ mlData }) {
  if (!mlData) return null;

  // Format top features for radar chart
  const topFeatures = Object.entries(mlData.top_features || {})
    .slice(0, 5)
    .map(([key, val]) => ({
      feature: key.replace('comp_', '').replace('evt_', ''),
      importance: Number((val * 100).toFixed(2))
    }));

  return (
    <div className="glass-card" style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.5rem' }}>
        <Brain color="var(--accent-color)" />
        <h2>Motor de Inteligencia Artificial</h2>
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1.5rem', padding: '1rem', background: 'rgba(255,255,255,0.05)', borderRadius: '8px' }}>
        <div>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', display: 'block' }}>Mejor Modelo</span>
          <span style={{ fontSize: '1.2rem', fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Award size={18} color="gold" /> {mlData.best_model}
          </span>
        </div>
        <div>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', display: 'block' }}>F1-Score Test</span>
          <span style={{ fontSize: '1.2rem', fontWeight: 'bold', color: 'var(--status-optimal)' }}>
            {(mlData.resultados_test[mlData.best_model].f1 * 100).toFixed(1)}%
          </span>
        </div>
        <div>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', display: 'block' }}>AUC-ROC</span>
          <span style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>
            {(mlData.resultados_test[mlData.best_model].auc_roc * 100).toFixed(1)}%
          </span>
        </div>
      </div>

      <h3 style={{ fontSize: '1rem', marginBottom: '1rem', color: 'var(--text-secondary)' }}>
        <Zap size={16} style={{ display: 'inline', verticalAlign: 'middle', marginRight: '5px' }}/>
        Importancia de Variables Clave
      </h3>
      
      <div style={{ flexGrow: 1, minHeight: '250px' }}>
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart cx="50%" cy="50%" outerRadius="70%" data={topFeatures}>
            <PolarGrid stroke="rgba(255,255,255,0.2)" />
            <PolarAngleAxis dataKey="feature" tick={{ fill: 'var(--text-secondary)', fontSize: 11 }} />
            <PolarRadiusAxis angle={30} domain={[0, 'auto']} tick={false} axisLine={false} />
            <Tooltip contentStyle={{ backgroundColor: 'var(--card-bg)', border: 'none', borderRadius: '8px', color: 'white' }} />
            <Radar name="Importancia (%)" dataKey="importance" stroke="var(--accent-color)" fill="var(--accent-color)" fillOpacity={0.5} />
          </RadarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
