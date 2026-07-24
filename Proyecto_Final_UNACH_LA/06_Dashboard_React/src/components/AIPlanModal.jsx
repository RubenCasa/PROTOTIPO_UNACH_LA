import React, { useState, useEffect, useRef } from 'react';
import { X, Bot, Sparkles, Printer, FileText, Download } from 'lucide-react';
import jsPDF from 'jspdf';

export default function AIPlanModal({ isOpen, onClose, studentData }) {
  const [step, setStep] = useState(0); // 0: loading, 1: typing, 2: done
  const [displayedText, setDisplayedText] = useState('');
  const [fullText, setFullText] = useState('');
  
  const textContainerRef = useRef(null);

  useEffect(() => {
    if (isOpen && studentData) {
      setStep(0);
      setDisplayedText('');
      setFullText('');
      
      // Intentar conectarse a la API Backend de Python
      fetch('http://localhost:8000/api/generar-plan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(studentData)
      })
      .then(res => {
        if(!res.ok) throw new Error('API Error');
        return res.json();
      })
      .then(data => {
        setFullText(data.plan);
        setStep(1);
      })
      .catch(err => {
        // Fallback local si el backend no está corriendo (ej. Vercel)
        setTimeout(() => {
          setFullText(`[SISTEMA IA UNACH-LA: INFORME GENERATIVO (MODO FALLBACK LOCAL)]\nEvaluando al estudiante ID: ${studentData.id_estudiante}\n\nANALIZANDO PATRONES...\n- Riesgo predictivo: ${studentData.probabilidad_riesgo_ml}%\n- Se detecta patrón anómalo.\n\n--- PLAN RECOMENDADO ---\n1. Citar al estudiante urgentemente.\n2. Asignar tutoría par.`);
          setStep(1);
        }, 1500);
      });
    }
  }, [isOpen, studentData]);

  useEffect(() => {
    if (step === 1 && fullText) {
      let i = 0;
      const intervalId = setInterval(() => {
        setDisplayedText(fullText.slice(0, i));
        i++;
        
        if (textContainerRef.current) {
          textContainerRef.current.scrollTop = textContainerRef.current.scrollHeight;
        }

        if (i > fullText.length) {
          clearInterval(intervalId);
          setStep(2);
        }
      }, 20);
      
      return () => clearInterval(intervalId);
    }
  }, [step, fullText]);

  const handleExportTxt = () => {
    const element = document.createElement("a");
    const file = new Blob([fullText], {type: 'text/plain'});
    element.href = URL.createObjectURL(file);
    element.download = `Plan_Intervencion_${studentData?.id_estudiante || 'UNACH'}.txt`;
    document.body.appendChild(element); 
    element.click();
  };

  const handleExportPDF = () => {
    const pdf = new jsPDF('p', 'mm', 'a4');
    pdf.setFont("helvetica", "normal");
    pdf.setFontSize(11);
    
    // Titulo
    pdf.setFont("helvetica", "bold");
    pdf.text(`Plan de Intervención IA - ID: ${studentData?.id_estudiante}`, 15, 20);
    
    pdf.setFont("helvetica", "normal");
    // Dividir texto largo para que encaje en el PDF
    const splitText = pdf.splitTextToSize(fullText, 180);
    pdf.text(splitText, 15, 30);
    
    pdf.save(`Plan_IA_${studentData?.id_estudiante || 'UNACH'}.pdf`);
  };

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
          <div className="ai-modal-footer fade-in" style={{ gap: '10px' }}>
            <button className="btn-secondary" onClick={onClose}>
              Cerrar
            </button>
            <button className="btn-ai-action" onClick={handleExportTxt} style={{ background: 'var(--text-muted)' }}>
              <FileText size={18} /> (.txt)
            </button>
            <button className="btn-ai-action" onClick={handleExportPDF}>
              <Download size={18} /> Exportar PDF Oficial
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
