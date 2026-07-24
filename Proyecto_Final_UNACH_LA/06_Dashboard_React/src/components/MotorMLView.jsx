import React, { useState } from 'react';
import Papa from 'papaparse';
import { UploadCloud, CheckCircle, Database } from 'lucide-react';

export default function MotorMLView() {
  const [dragActive, setDragActive] = useState(false);
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('idle'); // idle | processing | complete

  const handleDrag = function(e) {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = function(e) {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      processFile(e.dataTransfer.files[0]);
    }
  };

  const processFile = (file) => {
    setFile(file);
    setStatus('processing');
    
    // Simular procesamiento del Pipeline SICOA -> XGBoost
    setTimeout(() => {
      setStatus('complete');
    }, 3000);
  };

  return (
    <div className="glass-panel" style={{ minHeight: '600px', display: 'flex', flexDirection: 'column' }}>
      <div className="panel-title" style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <Database size={24} color="var(--accent-blue)" />
        <h2>Integración SICOA - Motor ML (XGBoost)</h2>
      </div>
      
      <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>
        Sube el historial académico extraído del Sistema Integrado de Control Académico (SICOA). 
        El modelo XGBoost procesará las notas, asistencias e historial para predecir nuevos riesgos y actualizar el Dashboard.
      </p>

      {status === 'idle' && (
        <div 
          className={`drop-zone ${dragActive ? 'drag-active' : ''}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          style={{
            flex: 1,
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            border: `2px dashed ${dragActive ? 'var(--accent-blue)' : 'var(--glass-border)'}`,
            borderRadius: '16px',
            backgroundColor: dragActive ? 'rgba(59, 130, 246, 0.05)' : 'rgba(0,0,0,0.2)',
            transition: 'all 0.3s ease',
            cursor: 'pointer'
          }}
          onClick={() => document.getElementById('file-upload').click()}
        >
          <UploadCloud size={64} color={dragActive ? 'var(--accent-blue)' : 'var(--text-muted)'} style={{ marginBottom: '1rem' }} />
          <h3 style={{ fontSize: '1.2rem', marginBottom: '0.5rem' }}>Arrastra y suelta tu archivo CSV o Excel aquí</h3>
          <p style={{ color: 'var(--text-muted)' }}>o haz clic para explorar en tu computadora</p>
          <input 
            type="file" 
            id="file-upload" 
            accept=".csv, .xlsx, .xls"
            style={{ display: 'none' }}
            onChange={(e) => {
              if (e.target.files && e.target.files[0]) {
                processFile(e.target.files[0]);
              }
            }}
          />
        </div>
      )}

      {status === 'processing' && (
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
          <div className="loading-state" style={{ height: 'auto', marginBottom: '2rem' }}>
            Procesando Pipeline XGBoost...
          </div>
          <p style={{ color: 'var(--text-muted)' }}>Analizando {file.name} - Extrayendo features de SICOA...</p>
        </div>
      )}

      {status === 'complete' && (
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', color: 'var(--status-green)' }}>
          <CheckCircle size={80} style={{ marginBottom: '1rem' }} />
          <h3 style={{ fontSize: '1.5rem', marginBottom: '0.5rem', color: 'var(--text-main)' }}>¡Análisis Completado!</h3>
          <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>El modelo ha generado las nuevas predicciones de riesgo.</p>
          
          <button 
            onClick={() => setStatus('idle')}
            style={{
              padding: '12px 24px',
              backgroundColor: 'var(--accent-blue)',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              fontSize: '1rem',
              cursor: 'pointer',
              fontWeight: '600'
            }}
          >
            Subir nuevo archivo
          </button>
        </div>
      )}
    </div>
  );
}
