import React, { useState, useEffect, useRef } from 'react';
import { Bot, Sparkles, Download, RefreshCw, AlertCircle } from 'lucide-react';
import jsPDF from 'jspdf';

export default function AIAnalysisPanel({ stats, sampleRows }) {
  const [status, setStatus] = useState('loading'); // loading | typing | done | error
  const [fullText, setFullText] = useState('');
  const [displayedText, setDisplayedText] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const textRef = useRef(null);

  const fetchAnalysis = async () => {
    setStatus('loading');
    setDisplayedText('');
    setFullText('');
    setErrorMsg('');

    // Build payload: send column stats + sample rows
    const payload = {
      fileName: stats.fileName,
      rowCount: stats.rowCount,
      colCount: stats.colCount,
      columns: Object.entries(stats.columns).map(([name, info]) => ({
        name,
        ...info,
      })),
      sampleRows: sampleRows.slice(0, 15),
    };

    try {
      // Try Vercel serverless function first
      let response;
      try {
        response = await fetch('/api/analyze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
      } catch {
        // If serverless fails (local dev), call Groq directly
        response = null;
      }

      if (response && response.ok) {
        const data = await response.json();
        setFullText(data.analysis);
        setStatus('typing');
      } else {
        // Fallback: Call Groq directly (for local dev only)
        const groqResponse = await fetch('https://api.groq.com/openai/v1/chat/completions', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${import.meta.env.VITE_GROQ_API_KEY || ''}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            model: 'llama-3.3-70b-versatile',
            messages: [
              {
                role: 'system',
                content: `Eres un experto en Learning Analytics y análisis de datos académicos de la Universidad Nacional de Chimborazo (UNACH). Tu rol es analizar datos del Sistema Integrado de Control Académico (SICOA) y plataforma Moodle para generar recomendaciones estratégicas para profesores y directivos académicos. Responde siempre en español.`
              },
              {
                role: 'user',
                content: `Analiza los siguientes datos académicos extraídos del archivo "${payload.fileName}":

RESUMEN DEL DATASET:
- Total de registros: ${payload.rowCount}
- Total de columnas: ${payload.colCount}

COLUMNAS DETECTADAS Y ESTADÍSTICAS:
${payload.columns.map(c => `• ${c.name} (${c.type}): ${c.nonEmpty} valores válidos, ${c.missing} faltantes${c.mean ? `, media=${c.mean}, min=${c.min}, max=${c.max}, desv=${c.stdDev}` : ''}`).join('\n')}

MUESTRA DE DATOS (primeras filas):
${JSON.stringify(payload.sampleRows.slice(0, 8), null, 2)}

Genera un análisis completo estructurado con estas secciones:

📊 RESUMEN GENERAL
Describe brevemente el dataset y su utilidad académica.

🎯 VARIABLES CLAVE PARA PREDICCIÓN DE RIESGO
Identifica qué columnas son más relevantes para predecir riesgo académico y por qué.

⚠️ ALERTAS Y ANOMALÍAS
Señala problemas en los datos (valores faltantes, distribuciones sesgadas, outliers potenciales).

📋 RECOMENDACIONES PARA EL PROFESOR
Da al menos 5 recomendaciones específicas y accionables basadas en los patrones detectados.

💡 SUGERENCIAS DE MEJORA
Propón mejoras al proceso de recolección de datos o seguimiento estudiantil.

Responde de forma profesional, concreta y en español.`
              }
            ],
            temperature: 0.7,
            max_tokens: 2500,
          }),
        });

        if (!groqResponse.ok) {
          const errData = await groqResponse.json().catch(() => ({}));
          throw new Error(errData.error?.message || `Error ${groqResponse.status} de Groq API`);
        }

        const groqData = await groqResponse.json();
        setFullText(groqData.choices[0].message.content);
        setStatus('typing');
      }
    } catch (err) {
      console.error('AI Analysis Error:', err);
      setErrorMsg(err.message || 'Error conectando con la IA. Verifica tu conexión o API key.');
      setStatus('error');
    }
  };

  // Initial fetch
  useEffect(() => {
    fetchAnalysis();
  }, []);

  // Typing effect
  useEffect(() => {
    if (status === 'typing' && fullText) {
      let i = 0;
      const speed = 12; // ms per character
      const intervalId = setInterval(() => {
        setDisplayedText(fullText.slice(0, i));
        i++;
        if (textRef.current) {
          textRef.current.scrollTop = textRef.current.scrollHeight;
        }
        if (i > fullText.length) {
          clearInterval(intervalId);
          setStatus('done');
        }
      }, speed);
      return () => clearInterval(intervalId);
    }
  }, [status, fullText]);

  const handleExportPDF = () => {
    const pdf = new jsPDF('p', 'mm', 'a4');
    pdf.setFont('helvetica', 'bold');
    pdf.setFontSize(14);
    pdf.text(`Análisis IA — ${stats.fileName}`, 15, 20);
    pdf.setFont('helvetica', 'normal');
    pdf.setFontSize(10);
    const lines = pdf.splitTextToSize(fullText, 180);
    pdf.text(lines, 15, 32);
    pdf.save(`Analisis_IA_${stats.fileName.replace(/\.[^/.]+$/, '')}.pdf`);
  };

  return (
    <div className="ai-analysis-panel fade-in">
      <div className="ai-analysis-header">
        <Bot size={28} color="#8b5cf6" />
        <div>
          <h3 style={{ fontSize: '1.1rem', margin: 0 }}>
            Análisis con IA — Groq (Llama 3.3-70B)
          </h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', margin: 0 }}>
            Análisis inteligente de tu archivo académico
          </p>
        </div>
      </div>

      {/* Loading */}
      {status === 'loading' && (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '3rem', gap: '1rem' }}>
          <Sparkles size={48} className="pulse-icon" color="#8b5cf6" />
          <p style={{ color: 'var(--text-muted)' }}>
            Conectando con Groq IA... Analizando {stats.rowCount} registros...
          </p>
          <div className="progress-bar-container" style={{ maxWidth: '300px' }}>
            <div className="progress-bar-fill slide-right" style={{ width: '100%' }} />
          </div>
        </div>
      )}

      {/* Error */}
      {status === 'error' && (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '3rem', gap: '1rem' }}>
          <AlertCircle size={48} color="var(--status-red)" />
          <p style={{ color: 'var(--status-red)', textAlign: 'center', maxWidth: '400px' }}>
            {errorMsg}
          </p>
          <button className="btn-primary" onClick={fetchAnalysis}>
            <RefreshCw size={16} /> Reintentar
          </button>
        </div>
      )}

      {/* Typing / Done */}
      {(status === 'typing' || status === 'done') && (
        <>
          <div
            ref={textRef}
            className="ai-text-container"
            style={{ maxHeight: '500px', marginTop: '1rem' }}
          >
            <pre className="ai-generated-text">{displayedText}</pre>
            {status === 'typing' && <span className="cursor-blink">|</span>}
          </div>

          {status === 'done' && (
            <div style={{ display: 'flex', gap: '10px', marginTop: '1.5rem', justifyContent: 'flex-end', flexWrap: 'wrap' }}>
              <button className="btn-secondary" onClick={fetchAnalysis}>
                <RefreshCw size={14} style={{ marginRight: 6 }} /> Regenerar
              </button>
              <button className="btn-ai-action" onClick={handleExportPDF}>
                <Download size={16} /> Exportar PDF
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
