import React, { useState } from 'react';
import Papa from 'papaparse';
import {
  UploadCloud,
  FileSpreadsheet,
  Table2,
  Sparkles,
  Download,
  Trash2,
  FileText,
  ChevronRight
} from 'lucide-react';
import AIAnalysisPanel from './AIAnalysisPanel';

export default function ImportExportView() {
  const [dragActive, setDragActive] = useState(false);
  const [file, setFile] = useState(null);
  const [parsedData, setParsedData] = useState(null);
  const [stats, setStats] = useState(null);
  const [showAIPanel, setShowAIPanel] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      processFile(e.dataTransfer.files[0]);
    }
  };

  const processFile = async (uploadedFile) => {
    const ext = uploadedFile.name.split('.').pop().toLowerCase();

    if (ext === 'csv') {
      Papa.parse(uploadedFile, {
        header: true,
        skipEmptyLines: true,
        complete: (results) => {
          finishParsing(uploadedFile, results.data, results.meta.fields || []);
        },
        error: (err) => console.error('Error parsing CSV:', err),
      });
    } else if (ext === 'xlsx' || ext === 'xls') {
      // Dynamic import of xlsx
      try {
        const XLSX = await import('xlsx');
        const reader = new FileReader();
        reader.onload = (e) => {
          const data = new Uint8Array(e.target.result);
          const workbook = XLSX.read(data, { type: 'array' });
          const firstSheet = workbook.SheetNames[0];
          const worksheet = workbook.Sheets[firstSheet];
          const jsonData = XLSX.utils.sheet_to_json(worksheet, { defval: '' });
          const headers = jsonData.length > 0 ? Object.keys(jsonData[0]) : [];
          finishParsing(uploadedFile, jsonData, headers);
        };
        reader.readAsArrayBuffer(uploadedFile);
      } catch (err) {
        console.error('Error parsing Excel:', err);
        alert('Error al leer el archivo Excel. Asegúrate de que el formato sea correcto.');
      }
    } else {
      alert('Formato no soportado. Usa CSV, XLS o XLSX.');
    }
  };

  const finishParsing = (uploadedFile, rows, columns) => {
    setFile(uploadedFile);
    setParsedData({ rows, columns });

    // Calculate statistics
    const colStats = {};
    columns.forEach((col) => {
      const values = rows.map((r) => r[col]).filter((v) => v !== '' && v !== null && v !== undefined);
      const numericValues = values.map(Number).filter((n) => !isNaN(n));

      colStats[col] = {
        type: numericValues.length > values.length * 0.7 ? 'numérica' : 'categórica',
        total: rows.length,
        nonEmpty: values.length,
        missing: rows.length - values.length,
        missingPct: (((rows.length - values.length) / rows.length) * 100).toFixed(1),
      };

      if (numericValues.length > 0) {
        const sum = numericValues.reduce((a, b) => a + b, 0);
        colStats[col].mean = (sum / numericValues.length).toFixed(2);
        colStats[col].min = Math.min(...numericValues).toFixed(2);
        colStats[col].max = Math.max(...numericValues).toFixed(2);
        const variance =
          numericValues.reduce((s, v) => s + Math.pow(v - sum / numericValues.length, 2), 0) /
          numericValues.length;
        colStats[col].stdDev = Math.sqrt(variance).toFixed(2);
      }
    });

    setStats({
      fileName: uploadedFile.name,
      fileSize: (uploadedFile.size / 1024).toFixed(1),
      rowCount: rows.length,
      colCount: columns.length,
      columns: colStats,
    });
  };

  const handleReset = () => {
    setFile(null);
    setParsedData(null);
    setStats(null);
    setShowAIPanel(false);
  };

  const handleExportCSV = () => {
    if (!parsedData) return;
    const csv = Papa.unparse(parsedData.rows);
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `analisis_${file.name}`;
    link.click();
  };

  return (
    <div className="fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <header className="header">
        <div>
          <h1>
            <FileSpreadsheet size={24} color="var(--text-accent)" style={{ marginRight: 10 }} />
            Importar & Exportar con IA
          </h1>
          <p>Sube tu archivo CSV o Excel para que la IA de Groq lo analice y genere recomendaciones.</p>
        </div>
      </header>

      {/* Upload Zone */}
      {!file && (
        <div
          className={`glass-panel drop-zone ${dragActive ? 'drag-active' : ''}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={() => document.getElementById('file-upload-ie').click()}
        >
          <UploadCloud
            size={56}
            className="pulse-icon"
            color={dragActive ? 'var(--text-accent)' : 'var(--text-muted)'}
            style={{ marginBottom: '1rem' }}
          />
          <h3 style={{ fontSize: '1.15rem', marginBottom: '0.5rem' }}>
            Arrastra y suelta tu archivo aquí
          </h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
            o haz clic para explorar • Soporta <strong>CSV, XLS, XLSX</strong>
          </p>
          <input
            type="file"
            id="file-upload-ie"
            accept=".csv,.xlsx,.xls"
            style={{ display: 'none' }}
            onChange={(e) => {
              if (e.target.files && e.target.files[0]) {
                processFile(e.target.files[0]);
              }
            }}
          />
        </div>
      )}

      {/* File Loaded */}
      {file && parsedData && stats && (
        <>
          {/* File Info Bar */}
          <div
            className="glass-panel"
            style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <FileSpreadsheet size={28} color="var(--text-accent)" />
              <div>
                <strong style={{ fontSize: '1rem' }}>{stats.fileName}</strong>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                  {stats.fileSize} KB • {stats.rowCount} filas • {stats.colCount} columnas
                </p>
              </div>
            </div>
            <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
              <button className="btn-secondary" onClick={handleExportCSV}>
                <Download size={14} style={{ marginRight: 6 }} /> Exportar CSV
              </button>
              <button
                className="btn-primary"
                onClick={() => setShowAIPanel(true)}
                disabled={showAIPanel}
                style={showAIPanel ? { opacity: 0.5, cursor: 'not-allowed' } : {}}
              >
                <Sparkles size={16} /> Analizar con IA
                <ChevronRight size={16} />
              </button>
              <button
                className="btn-secondary"
                onClick={handleReset}
                style={{ borderColor: 'rgba(239,68,68,0.2)', color: 'var(--status-red)' }}
              >
                <Trash2 size={14} />
              </button>
            </div>
          </div>

          {/* Column Stats */}
          <div className="glass-panel">
            <h3 className="panel-title" style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <Table2 size={18} color="var(--text-accent)" />
              Estadísticas por Columna
            </h3>
            <div className="table-container" style={{ maxHeight: '250px' }}>
              <table>
                <thead>
                  <tr>
                    <th>Columna</th>
                    <th>Tipo</th>
                    <th>No Vacíos</th>
                    <th>Faltantes</th>
                    <th>Media</th>
                    <th>Min</th>
                    <th>Max</th>
                    <th>Desv. Est.</th>
                  </tr>
                </thead>
                <tbody>
                  {parsedData.columns.map((col) => {
                    const s = stats.columns[col];
                    return (
                      <tr key={col}>
                        <td><strong>{col}</strong></td>
                        <td>
                          <span className={`badge ${s.type === 'numérica' ? 'badge-blue' : 'badge-yellow'}`}>
                            {s.type}
                          </span>
                        </td>
                        <td>{s.nonEmpty}</td>
                        <td>
                          {s.missing > 0 ? (
                            <span style={{ color: 'var(--status-red)' }}>{s.missing} ({s.missingPct}%)</span>
                          ) : (
                            <span style={{ color: 'var(--status-green)' }}>0</span>
                          )}
                        </td>
                        <td>{s.mean || '—'}</td>
                        <td>{s.min || '—'}</td>
                        <td>{s.max || '—'}</td>
                        <td>{s.stdDev || '—'}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>

          {/* Data Preview */}
          <div className="glass-panel">
            <h3 className="panel-title" style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <FileText size={18} color="var(--text-accent)" />
              Vista Previa (primeras 10 filas)
            </h3>
            <div className="file-preview-table">
              <table>
                <thead>
                  <tr>
                    <th>#</th>
                    {parsedData.columns.map((col) => (
                      <th key={col}>{col}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {parsedData.rows.slice(0, 10).map((row, i) => (
                    <tr key={i}>
                      <td style={{ color: 'var(--text-muted)' }}>{i + 1}</td>
                      {parsedData.columns.map((col) => (
                        <td key={col}>{row[col] ?? ''}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* AI Analysis Panel */}
          {showAIPanel && (
            <AIAnalysisPanel stats={stats} sampleRows={parsedData.rows.slice(0, 20)} />
          )}
        </>
      )}
    </div>
  );
}
