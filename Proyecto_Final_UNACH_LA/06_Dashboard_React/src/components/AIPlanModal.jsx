import React, { useState, useEffect, useRef } from 'react';
import { X, Bot, Sparkles, Printer, FileText } from 'lucide-react';

export default function AIPlanModal({ isOpen, onClose, studentData }) {
  const [step, setStep] = useState(0); // 0: loading, 1: typing, 2: done
  const [displayedText, setDisplayedText] = useState('');
  
  // Ref para el contenedor del texto y poder hacer auto-scroll
  const textContainerRef = useRef(null);

  // Texto simulado del LLM
  const fullText = `[SISTEMA IA UNACH-LA: INFORME GENERATIVO DE INTERVENCIÓN]
Evaluando al estudiante ID: ${studentData?.id_estudiante || 'N/A'} (Carrera: ${studentData?.carrera || 'N/A'})
Probabilidad de Riesgo Predictiva: ${studentData?.probabilidad_riesgo_ml || '0'}%

ANALIZANDO PATRONES...
- Se ha detectado una caída significativa en la asistencia durante el último mes.
- El rendimiento en materias de especialidad (ciencias exactas) está por debajo de la desviación estándar de su cohorte.
- El modelo XGBoost clasifica este patrón como de ALTA probabilidad de abandono prematuro.

--- PLAN DE ACCIÓN RECOMENDADO ---

1. INTERVENCIÓN TEMPRANA (Próximas 48 Horas):
El Coordinador de Carrera debe citar al estudiante para una tutoría diagnóstica personalizada. Objetivo: Identificar barreras externas (económicas/psicológicas).

2. APOYO ACADÉMICO:
Asignar de manera inmediata al estudiante a los talleres de nivelación de los días Viernes. Asignar un estudiante de semestres superiores como mentor par.

3. MONITOREO SICOA:
Configurar una alerta de seguimiento a 15 días. Si las calificaciones del primer parcial no superan el 7/10, derivar el caso al Departamento de Bienestar Estudiantil.

[Fin de la generación del plan. Documento listo para exportación PDF o envío a autoridades.]`;

  useEffect(() => {
    if (isOpen) {
      setStep(0);
      setDisplayedText('');
      
      // Simular tiempo de carga/pensamiento del modelo
      const loadingTimer = setTimeout(() => {
        setStep(1);
      }, 1500);
      
      return () => clearTimeout(loadingTimer);
    }
  }, [isOpen]);

  useEffect(() => {
    if (step === 1) {
      let i = 0;
      const intervalId = setInterval(() => {
        setDisplayedText(fullText.slice(0, i));
        i++;
        
        // Auto scroll hacia abajo
        if (textContainerRef.current) {
          textContainerRef.current.scrollTop = textContainerRef.current.scrollHeight;
        }

        if (i > fullText.length) {
          clearInterval(intervalId);
          setStep(2);
        }
      }, 20); // Velocidad de escritura
      
      return () => clearInterval(intervalId);
    }
  }, [step, fullText]);

  if (!isOpen) return null;

  return (
    <div className="modal-backdrop fade-in" onClick={onClose}>
      <div className="ai-modal slide-up" onClick={e => e.stopPropagation()}>
        
        {/* Cabecera del Modal */}
        <div className="ai-modal-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Bot size={28} color="var(--accent-purple)" />
            <h2 style={{ fontSize: '1.2rem', margin: 0 }}>Generador de Planes IA</h2>
          </div>
          <button className="close-btn" onClick={onClose}><X size={24} /></button>
        </div>

        {/* Cuerpo del Modal */}
        <div className="ai-modal-body">
          {step === 0 && (
            <div className="ai-loading">
              <Sparkles size={48} className="pulse-icon" color="var(--accent-purple)" />
              <p>Analizando datos del estudiante y entrenando plan óptimo...</p>
            </div>
          )}

          {(step === 1 || step === 2) && (
            <div className="ai-text-container" ref={textContainerRef}>
              <pre className="ai-generated-text">{displayedText}</pre>
              {step === 1 && <span className="cursor-blink">|</span>}
            </div>
          )}
        </div>

        {/* Pie del Modal */}
        {step === 2 && (
          <div className="ai-modal-footer fade-in">
            <button className="btn-secondary" onClick={onClose}>
              Cerrar
            </button>
            <button className="btn-ai-action">
              <FileText size={18} /> Exportar Plan a SICOA
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
