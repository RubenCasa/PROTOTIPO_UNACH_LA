import React from 'react';
import { X, Users } from 'lucide-react';
import { Radar } from 'react-chartjs-2';
import { Chart as ChartJS, RadialLinearScale, PointElement, LineElement, Filler, Tooltip as ChartTooltip, Legend } from 'chart.js';

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, ChartTooltip, Legend);

export default function CompareStudentsModal({ isOpen, onClose, students }) {
  if (!isOpen || !students || students.length !== 2) return null;

  const [studentA, studentB] = students;

  const data = {
    labels: ['Asistencia', 'Notas Especialidad', 'Notas Generales', 'Participación', 'Cumplimiento Tareas', 'Interacción SICOA'],
    datasets: [
      {
        label: `Estudiante A: ${studentA.id_estudiante}`,
        data: [
          Math.floor(Math.random() * 40) + 40,
          Math.floor(Math.random() * 40) + 40,
          Math.floor(Math.random() * 40) + 50,
          Math.floor(Math.random() * 40) + 30,
          Math.floor(Math.random() * 40) + 60,
          Math.floor(Math.random() * 40) + 40,
        ],
        backgroundColor: 'rgba(2, 132, 199, 0.2)', // UNACH Blue
        borderColor: 'rgba(2, 132, 199, 1)',
        borderWidth: 2,
        pointBackgroundColor: 'rgba(2, 132, 199, 1)',
      },
      {
        label: `Estudiante B: ${studentB.id_estudiante}`,
        data: [
          Math.floor(Math.random() * 40) + 40,
          Math.floor(Math.random() * 40) + 40,
          Math.floor(Math.random() * 40) + 50,
          Math.floor(Math.random() * 40) + 30,
          Math.floor(Math.random() * 40) + 60,
          Math.floor(Math.random() * 40) + 40,
        ],
        backgroundColor: 'rgba(225, 29, 72, 0.2)', // UNACH Red
        borderColor: 'rgba(225, 29, 72, 1)',
        borderWidth: 2,
        pointBackgroundColor: 'rgba(225, 29, 72, 1)',
      }
    ],
  };

  const options = {
    scales: {
      r: {
        angleLines: { color: 'rgba(0, 0, 0, 0.1)' },
        grid: { color: 'rgba(0, 0, 0, 0.1)' },
        pointLabels: { color: '#64748b', font: { size: 12, family: 'Inter' } },
        ticks: { display: false, min: 0, max: 100 }
      }
    },
    plugins: {
      legend: { labels: { color: '#0f172a' }, position: 'bottom' }
    }
  };

  return (
    <div className="modal-backdrop fade-in" onClick={onClose}>
      <div className="ai-modal slide-up" onClick={e => e.stopPropagation()} style={{ maxWidth: '800px', flexDirection: 'column' }}>
        
        <div className="ai-modal-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Users color="var(--accent-blue)" />
            <h3 style={{ margin: 0, color: 'var(--text-main)' }}>A/B Testing: Comparativa Académica</h3>
          </div>
          <button className="close-btn" onClick={onClose}><X size={24} /></button>
        </div>

        <div style={{ display: 'flex', flex: 1 }}>
          <div style={{ flex: 1, padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1.5rem', borderRight: '1px solid var(--glass-border)' }}>
            
            {/* Student A Details */}
            <div style={{ padding: '1rem', background: 'rgba(2, 132, 199, 0.05)', borderRadius: '8px', borderLeft: '4px solid rgba(2, 132, 199, 1)' }}>
              <h4 style={{ color: 'rgba(2, 132, 199, 1)', margin: '0 0 0.5rem 0' }}>{studentA.id_estudiante}</h4>
              <p style={{ margin: 0, fontSize: '0.85rem', color: 'var(--text-muted)' }}>{studentA.carrera}</p>
              <div style={{ marginTop: '0.5rem', fontWeight: 'bold' }}>Riesgo: {studentA.probabilidad_riesgo_ml}% ({studentA.nivel_riesgo})</div>
            </div>

            {/* Student B Details */}
            <div style={{ padding: '1rem', background: 'rgba(225, 29, 72, 0.05)', borderRadius: '8px', borderLeft: '4px solid rgba(225, 29, 72, 1)' }}>
              <h4 style={{ color: 'rgba(225, 29, 72, 1)', margin: '0 0 0.5rem 0' }}>{studentB.id_estudiante}</h4>
              <p style={{ margin: 0, fontSize: '0.85rem', color: 'var(--text-muted)' }}>{studentB.carrera}</p>
              <div style={{ marginTop: '0.5rem', fontWeight: 'bold' }}>Riesgo: {studentB.probabilidad_riesgo_ml}% ({studentB.nivel_riesgo})</div>
            </div>

            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: 'auto' }}>
              Esta comparativa multicriterio ayuda a identificar fortalezas relativas y guiar tutorías de pares.
            </p>
          </div>

          <div style={{ flex: 1.5, padding: '2rem', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
             <div style={{ width: '100%', maxWidth: '400px' }}>
                <Radar data={data} options={options} />
             </div>
          </div>
        </div>

      </div>
    </div>
  );
}
