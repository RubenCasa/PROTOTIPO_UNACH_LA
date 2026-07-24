import React from 'react';
import { AlertCircle, Search } from 'lucide-react';

export default function AlertsTable({ alerts }) {
  if (!alerts || alerts.length === 0) return null;

  return (
    <div className="glass-card" style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <AlertCircle color="var(--status-critical)" />
          <h2>Alertas Prioritarias</h2>
        </div>
        <div style={{ background: 'rgba(255,255,255,0.1)', padding: '0.5rem 1rem', borderRadius: '20px', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Search size={16} color="var(--text-secondary)" />
          <input 
            type="text" 
            placeholder="Buscar ID..." 
            style={{ background: 'transparent', border: 'none', color: 'white', outline: 'none', width: '120px' }}
          />
        </div>
      </div>

      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid var(--card-border)', color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
              <th style={{ padding: '1rem 0.5rem' }}>Estudiante ID</th>
              <th style={{ padding: '1rem 0.5rem' }}>Nota</th>
              <th style={{ padding: '1rem 0.5rem' }}>Asistencia</th>
              <th style={{ padding: '1rem 0.5rem' }}>Riesgo ML</th>
              <th style={{ padding: '1rem 0.5rem' }}>Nivel</th>
            </tr>
          </thead>
          <tbody>
            {alerts.slice(0, 7).map((alert, idx) => (
              <tr key={idx} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)', transition: 'background 0.2s', cursor: 'pointer' }} 
                  onMouseOver={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.05)'}
                  onMouseOut={(e) => e.currentTarget.style.background = 'transparent'}
              >
                <td style={{ padding: '1rem 0.5rem', fontWeight: '500' }}>{alert.id_estudiante}</td>
                <td style={{ padding: '1rem 0.5rem' }}>{alert.nota_actual}</td>
                <td style={{ padding: '1rem 0.5rem' }}>{alert.porcentaje_asistencia}%</td>
                <td style={{ padding: '1rem 0.5rem' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <div style={{ width: '100%', background: 'rgba(255,255,255,0.1)', height: '6px', borderRadius: '3px', overflow: 'hidden' }}>
                      <div style={{ 
                        width: `${alert.probabilidad_riesgo_ml}%`, 
                        height: '100%', 
                        background: alert.probabilidad_riesgo_ml > 75 ? 'var(--status-critical)' : 'var(--status-warning)'
                      }}></div>
                    </div>
                    <span style={{ fontSize: '0.8rem' }}>{alert.probabilidad_riesgo_ml.toFixed(0)}%</span>
                  </div>
                </td>
                <td style={{ padding: '1rem 0.5rem' }}>
                  <span style={{ 
                    padding: '0.2rem 0.6rem', 
                    borderRadius: '12px', 
                    fontSize: '0.75rem', 
                    fontWeight: 'bold',
                    backgroundColor: alert.nivel_riesgo === 'ALTO' ? 'rgba(239, 68, 68, 0.2)' : 'rgba(245, 158, 11, 0.2)',
                    color: alert.nivel_riesgo === 'ALTO' ? '#fca5a5' : '#fcd34d'
                  }}>
                    {alert.nivel_riesgo}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {alerts.length > 7 && (
        <div style={{ textAlign: 'center', marginTop: '1rem' }}>
          <button style={{ 
            background: 'transparent', 
            border: '1px solid var(--accent-color)', 
            color: 'var(--accent-color)', 
            padding: '0.5rem 1rem', 
            borderRadius: '8px', 
            cursor: 'pointer',
            transition: 'all 0.2s'
          }}
          onMouseOver={(e) => { e.currentTarget.style.background = 'var(--accent-color)'; e.currentTarget.style.color = 'white'; }}
          onMouseOut={(e) => { e.currentTarget.style.background = 'transparent'; e.currentTarget.style.color = 'var(--accent-color)'; }}
          >
            Ver todas las alertas (+{alerts.length - 7})
          </button>
        </div>
      )}
    </div>
  );
}
