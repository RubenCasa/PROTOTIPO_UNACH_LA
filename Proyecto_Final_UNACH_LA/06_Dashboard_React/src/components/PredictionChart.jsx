import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip as ChartTooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, ChartTooltip, Legend);

export default function PredictionChart() {
  const data = {
    labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago (Pred)', 'Sep (Pred)', 'Oct (Pred)', 'Nov (Pred)', 'Dic (Pred)'],
    datasets: [
      {
        label: 'Promedio Histórico SICOA (Escala 1-10)',
        data: [7.8, 7.9, 7.5, 7.2, 7.4, 7.6, 7.5, null, null, null, null, null],
        borderColor: 'rgba(59, 130, 246, 1)',
        backgroundColor: 'rgba(59, 130, 246, 0.5)',
        tension: 0.4,
        borderWidth: 2,
        pointRadius: 4,
      },
      {
        label: 'Proyección Modelo XGBoost (Tendencia de Riesgo)',
        data: [null, null, null, null, null, null, 7.5, 7.3, 6.9, 6.4, 5.8, 5.1],
        borderColor: 'rgba(239, 68, 68, 1)',
        backgroundColor: 'rgba(239, 68, 68, 0.5)',
        borderDash: [5, 5], // Línea punteada
        tension: 0.4,
        borderWidth: 2,
        pointRadius: 4,
        pointBackgroundColor: 'var(--status-red)'
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: 'index',
      intersect: false,
    },
    plugins: {
      legend: {
        position: 'top',
        labels: { color: '#0f172a' }
      },
      tooltip: {
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        titleColor: '#0f172a',
        bodyColor: '#334155',
        borderColor: 'rgba(0,0,0,0.1)',
        borderWidth: 1
      }
    },
    scales: {
      x: {
        grid: { color: 'rgba(0, 0, 0, 0.05)' },
        ticks: { color: '#64748b' }
      },
      y: {
        grid: { color: 'rgba(0, 0, 0, 0.05)' },
        ticks: { color: '#64748b' },
        min: 0,
        max: 10
      }
    }
  };

  return (
    <div className="glass-panel fade-in" style={{ height: '400px', display: 'flex', flexDirection: 'column', marginTop: '2rem' }}>
      <h3 className="panel-title">Predicción de Trayectoria Global (Series Temporales)</h3>
      <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '1rem' }}>
        El modelo proyecta una caída sostenida en los promedios globales si no se aplican los planes de intervención a tiempo.
      </p>
      <div style={{ flex: 1, position: 'relative' }}>
        <Line data={data} options={options} />
      </div>
    </div>
  );
}
