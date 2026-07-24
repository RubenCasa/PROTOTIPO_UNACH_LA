import React, { useState } from 'react';
import AIPlanModal from './AIPlanModal';
import StudentProfileModal from './StudentProfileModal';
import CompareStudentsModal from './CompareStudentsModal';
import { Sparkles, User, GitCompare } from 'lucide-react';

export default function AlertsTable({ data }) {
  const [isAIModalOpen, setIsAIModalOpen] = useState(false);
  const [isProfileModalOpen, setIsProfileModalOpen] = useState(false);
  const [isCompareModalOpen, setIsCompareModalOpen] = useState(false);
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [selectedForComparison, setSelectedForComparison] = useState([]);

  const topAlerts = data.slice(0, 15);

  const handleCheckboxChange = (student) => {
    setSelectedForComparison(prev => {
      if (prev.find(s => s.id_estudiante === student.id_estudiante)) {
        return prev.filter(s => s.id_estudiante !== student.id_estudiante);
      } else {
        if (prev.length < 2) return [...prev, student];
        return prev; // Max 2
      }
    });
  };

  const handleOpenCompare = () => {
    if (selectedForComparison.length === 2) {
      setIsCompareModalOpen(true);
    }
  };

  const handleOpenAIPlan = (student) => {
    setSelectedStudent(student);
    setIsAIModalOpen(true);
  };

  const handleOpenProfile = (student) => {
    setSelectedStudent(student);
    setIsProfileModalOpen(true);
  };

  return (
    <>
      <div className="glass-panel" style={{ position: 'relative' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h3 className="panel-title">Estudiantes en Riesgo Crítico (Top Prioridad)</h3>
          
          {selectedForComparison.length === 2 && (
            <button 
              onClick={handleOpenCompare}
              className="btn-ai-sparkle fade-in" 
              style={{ background: 'var(--accent-gradient)', color: 'white', padding: '0.5rem 1rem' }}
            >
              <GitCompare size={16} /> Comparar Estudiantes (A/B)
            </button>
          )}
        </div>
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th style={{ width: '40px' }}></th>
                <th>ID Estudiante</th>
                <th>Riesgo ML</th>
                <th>Semáforo</th>
                <th>Acción Recomendada</th>
                <th>Inteligencia Artificial</th>
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
                  <tr key={index} style={{ background: selectedForComparison.find(s => s.id_estudiante === alerta.id_estudiante) ? 'rgba(2, 132, 199, 0.05)' : '' }}>
                    <td>
                      <input 
                        type="checkbox" 
                        checked={!!selectedForComparison.find(s => s.id_estudiante === alerta.id_estudiante)}
                        onChange={() => handleCheckboxChange(alerta)}
                        disabled={selectedForComparison.length >= 2 && !selectedForComparison.find(s => s.id_estudiante === alerta.id_estudiante)}
                        style={{ cursor: 'pointer', transform: 'scale(1.2)' }}
                        title="Seleccionar para comparar (Máx 2)"
                      />
                    </td>
                    <td>
                      <button 
                        onClick={() => handleOpenProfile(alerta)}
                        style={{ background: 'none', border: 'none', textAlign: 'left', cursor: 'pointer', display: 'flex', flexDirection: 'column', gap: '2px' }}
                        className="student-id-btn"
                        title="Ver Perfil 360°"
                      >
                        <strong style={{ display: 'flex', alignItems: 'center', gap: '5px', color: 'var(--accent-blue)', textDecoration: 'underline' }}>
                          <User size={14} /> {alerta.id_estudiante}
                        </strong>
                        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                          {alerta.carrera}
                        </span>
                      </button>
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
                    <td style={{ fontSize: '0.8rem', maxWidth: '180px' }}>
                      {alerta.accion_recomendada}
                    </td>
                    <td>
                      <button 
                        className="btn-ai-sparkle" 
                        onClick={() => handleOpenAIPlan(alerta)}
                        title="Generar Plan de Rescate con IA"
                      >
                        <Sparkles size={16} /> Plan IA
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      <AIPlanModal 
        isOpen={isAIModalOpen} 
        onClose={() => setIsAIModalOpen(false)} 
        studentData={selectedStudent} 
      />

      <StudentProfileModal
        isOpen={isProfileModalOpen}
        onClose={() => setIsProfileModalOpen(false)}
        studentData={selectedStudent}
      />

      <CompareStudentsModal
        isOpen={isCompareModalOpen}
        onClose={() => setIsCompareModalOpen(false)}
        students={selectedForComparison}
      />
    </>
  );
}
