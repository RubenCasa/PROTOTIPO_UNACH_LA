import React from 'react';

export default function AlertsTable({ data }) {
  const topAlerts = data.slice(0, 15);

  return (
    <div className="glass-panel">
      <h3 className="panel-title">Estudiantes en Riesgo Crítico (Top Prioridad)</h3>
      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>ID Estudiante</th>
              <th>Riesgo ML</th>
              <th>Semáforo</th>
              <th>Acción Recomendada</th>
            </tr>
          </thead>
          <tbody>
            {topAlerts.map((alerta, index) => {
              let color = 'var(--status-green)';
              if (alerta.nivel_riesgo === 'ALTO') color = 'var(--status-red)';
              if (alerta.nivel_riesgo === 'MEDIO') color = 'var(--status-yellow)';

              let badge = 'badge-green';
              if (alerta.nivel_riesgo === 'ALTO') badge = 'badge-red';
              if (alerta.nivel_riesgo === 'MEDIO') badge = 'badge-yellow';

              return (
                <tr key={index}>
                  <td>
                    <strong>{alerta.id_estudiante}</strong><br/>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                      {alerta.carrera}
                    </span>
                  </td>
                  <td>
                    {alerta.probabilidad_riesgo_ml}%
                    <div className="risk-bar-bg">
                      <div className="risk-bar-fill" style={{ width: `${alerta.probabilidad_riesgo_ml}%`, backgroundColor: color }}></div>
                    </div>
                  </td>
                  <td>
                    <span className={`badge ${badge}`}>
                      {alerta.semaforo.split(' ')[0]}
                    </span>
                  </td>
                  <td style={{ fontSize: '0.8rem', maxWidth: '200px' }}>
                    {alerta.accion_recomendada}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
