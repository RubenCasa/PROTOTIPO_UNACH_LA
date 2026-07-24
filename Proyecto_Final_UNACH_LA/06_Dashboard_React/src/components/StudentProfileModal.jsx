import React, { useRef } from 'react';
import { X, UserCheck, AlertTriangle, Download } from 'lucide-react';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import { Radar } from 'react-chartjs-2';
import { Chart as ChartJS, RadialLinearScale, PointElement, LineElement, Filler, Tooltip as ChartTooltip, Legend } from 'chart.js';

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, ChartTooltip, Legend);

export default function StudentProfileModal({ isOpen, onClose, studentData }) {
  const modalRef = useRef(null);

  if (!isOpen || !studentData) return null;

  const handleDownloadPDF = async () => {
    if (!modalRef.current) return;
    
    // Ocultar botón de cierre durante captura
    const closeBtn = modalRef.current.querySelector('.close-btn');
    const downloadBtn = modalRef.current.querySelector('.download-pdf-btn');
    if(closeBtn) closeBtn.style.display = 'none';
    if(downloadBtn) downloadBtn.style.display = 'none';

    try {
      const canvas = await html2canvas(modalRef.current, { scale: 2 });
      const imgData = canvas.toDataURL('image/png');
      
      const pdf = new jsPDF('l', 'mm', 'a4'); // Orientación horizontal
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (canvas.height * pdfWidth) / canvas.width;
      
      pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
      pdf.save(`Expediente_${studentData.id_estudiante}.pdf`);
    } catch (error) {
      console.error('Error generando PDF', error);
    } finally {
      if(closeBtn) closeBtn.style.display = 'block';
      if(downloadBtn) downloadBtn.style.display = 'flex';
    }
  };

  const data = {
    labels: ['Asistencia', 'Notas Especialidad', 'Notas Generales', 'Participación', 'Cumplimiento Tareas', 'Interacción SICOA'],
    datasets: [
      {
        label: 'Perfil del Estudiante',
        data: [
          Math.floor(Math.random() * 40) + 40, // Simulación de datos basados en riesgo
          Math.floor(Math.random() * 40) + 40,
          Math.floor(Math.random() * 40) + 50,
          Math.floor(Math.random() * 40) + 30,
          Math.floor(Math.random() * 40) + 60,
          Math.floor(Math.random() * 40) + 40,
        ],
        backgroundColor: 'rgba(59, 130, 246, 0.2)',
        borderColor: 'rgba(59, 130, 246, 1)',
        borderWidth: 2,
        pointBackgroundColor: 'rgba(139, 92, 246, 1)',
      },
      {
        label: 'Promedio de Cohorte',
        data: [85, 80, 85, 75, 90, 80],
        backgroundColor: 'rgba(148, 163, 184, 0.1)',
        borderColor: 'rgba(148, 163, 184, 0.5)',
        borderWidth: 1,
        borderDash: [5, 5]
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
      legend: { labels: { color: '#0f172a' } }
    }
  };

  return (
    <div className="modal-backdrop fade-in" onClick={onClose}>
      <div className="ai-modal slide-up" onClick={e => e.stopPropagation()} style={{ maxWidth: '900px', flexDirection: 'row' }} ref={modalRef}>
        
        {/* Left Side: Info */}
        <div style={{ flex: 1, padding: '2rem', borderRight: '1px solid var(--glass-border)', background: 'rgba(0,0,0,0.2)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div style={{ width: '80px', height: '80px', borderRadius: '50%', background: 'var(--accent-gradient)', display: 'flex', justifyContent: 'center', alignItems: 'center', marginBottom: '1.5rem', boxShadow: '0 0 20px rgba(59, 130, 246, 0.4)' }}>
              <UserCheck size={40} color="white" />
            </div>
          </div>
          <h2 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>{studentData.id_estudiante}</h2>
          <p style={{ color: 'var(--accent-purple)', fontWeight: '600', marginBottom: '2rem' }}>{studentData.carrera}</p>
          
          <div style={{ marginBottom: '1.5rem' }}>
            <h4 style={{ color: 'var(--text-muted)', fontSize: '0.85rem', textTransform: 'uppercase', marginBottom: '0.5rem' }}>Probabilidad Riesgo (XGBoost)</h4>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={{ fontSize: '2.5rem', fontWeight: '800', color: studentData.nivel_riesgo === 'ALTO' ? 'var(--status-red)' : 'var(--status-yellow)' }}>
                {studentData.probabilidad_riesgo_ml}%
              </span>
              <AlertTriangle color={studentData.nivel_riesgo === 'ALTO' ? 'var(--status-red)' : 'var(--status-yellow)'} size={32} />
            </div>
          </div>

          <div>
            <h4 style={{ color: 'var(--text-muted)', fontSize: '0.85rem', textTransform: 'uppercase', marginBottom: '0.5rem' }}>Acción Recomendada</h4>
            <p style={{ fontSize: '0.9rem', lineHeight: '1.5', background: 'rgba(0,0,0,0.03)', padding: '1rem', borderRadius: '8px' }}>
              {studentData.accion_recomendada}
            </p>
          </div>

          <button 
            className="download-pdf-btn btn-ai-sparkle" 
            onClick={handleDownloadPDF}
            style={{ marginTop: '2rem', width: '100%', justifyContent: 'center', background: 'var(--text-main)', color: 'white' }}
          >
            <Download size={16} /> Exportar Expediente a PDF
          </button>
        </div>

        {/* Right Side: Radar Chart */}
        <div style={{ flex: 1.5, padding: '2rem', display: 'flex', flexDirection: 'column' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h3 style={{ fontSize: '1.2rem' }}>Perfil 360° Académico</h3>
            <button className="close-btn" onClick={onClose}><X size={24} /></button>
          </div>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '2rem' }}>
            Comparativa multicriterio frente a la cohorte histórica del SICOA.
          </p>
          <div style={{ flex: 1, display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            <div style={{ width: '100%', maxWidth: '400px' }}>
              <Radar data={data} options={options} />
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
