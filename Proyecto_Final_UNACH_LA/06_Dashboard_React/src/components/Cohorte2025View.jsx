import React, { useState, useEffect } from 'react';
import Papa from 'papaparse';
import {
  FileText,
  BarChart2,
  Users,
  Activity,
  Sparkles,
  Loader
} from 'lucide-react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Scatter, Bar } from 'react-chartjs-2';
import AIAnalysisPanel from './AIAnalysisPanel';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export default function Cohorte2025View() {
  const [sicoaData, setSicoaData] = useState([]);
  const [moodleData, setMoodleData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  // Stats
  const [stats, setStats] = useState({
    totalStudents: 0,
    avgAttendance: 0,
    avgGrade: 0,
    totalMoodleEvents: 0
  });

  // Fused payload for AI
  const [fusedSample, setFusedSample] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      // 1. Fetch SICOA
      const sicoaRes = await fetch('/datasets/SICOA_Anonimizado_Listo.csv');
      if (!sicoaRes.ok) throw new Error("No se pudo cargar SICOA_Anonimizado_Listo.csv");
      const sicoaCsv = await sicoaRes.text();
      const sicoaParsed = Papa.parse(sicoaCsv, { header: true, skipEmptyLines: true });
      
      // 2. Fetch Moodle
      const moodleRes = await fetch('/datasets/Moodle_Anonimizado_Listo.csv');
      if (!moodleRes.ok) throw new Error("No se pudo cargar Moodle_Anonimizado_Listo.csv");
      const moodleCsv = await moodleRes.text();
      const moodleParsed = Papa.parse(moodleCsv, { header: true, skipEmptyLines: true });

      setSicoaData(sicoaParsed.data);
      setMoodleData(moodleParsed.data);
      
      calculateStats(sicoaParsed.data, moodleParsed.data);
      
      // Prepare a fused sample for the AI Analysis panel
      setFusedSample({
        columns: ['ID_Estudiante', 'PromedioFinalNumero', 'TotalPorcentajeAsistencia', 'MoodleEventos'],
        rows: sicoaParsed.data.slice(0, 50).map(row => ({
          ID_Estudiante: row.ID_Estudiante,
          PromedioFinalNumero: row.PromedioFinalNumero,
          TotalPorcentajeAsistencia: row.TotalPorcentajeAsistencia,
          MoodleEventos: 'N/A' // Sample data
        }))
      });

    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const calculateStats = (sicoa, moodle) => {
    let validGrades = 0;
    let sumGrades = 0;
    let validAtt = 0;
    let sumAtt = 0;

    sicoa.forEach(row => {
      const grade = parseFloat(row.PromedioFinalNumero);
      const att = parseFloat(row.TotalPorcentajeAsistencia);
      if (!isNaN(grade)) { sumGrades += grade; validGrades++; }
      if (!isNaN(att)) { sumAtt += att; validAtt++; }
    });

    setStats({
      totalStudents: sicoa.length,
      avgGrade: validGrades > 0 ? (sumGrades / validGrades).toFixed(2) : 0,
      avgAttendance: validAtt > 0 ? (sumAtt / validAtt).toFixed(1) : 0,
      totalMoodleEvents: moodle.length
    });
  };

  if (loading) {
    return (
      <div className="fade-in" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '60vh' }}>
        <Loader className="pulse-icon" size={48} color="var(--text-accent)" style={{ animation: 'spin 2s linear infinite' }} />
        <h2 style={{ marginTop: '1rem' }}>Cargando Cohorte 2025...</h2>
        <p style={{ color: 'var(--text-muted)' }}>Leyendo y procesando miles de registros localmente</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="fade-in" style={{ padding: '2rem', textAlign: 'center' }}>
        <h2 style={{ color: 'var(--status-red)' }}>Error al cargar los datos</h2>
        <p>{error}</p>
        <p>Asegúrate de que los archivos estén en `public/datasets/`.</p>
      </div>
    );
  }

  // Preparar datos para Scatter (Asistencia vs Nota)
  const scatterData = {
    datasets: [
      {
        label: 'Estudiantes',
        data: sicoaData.slice(0, 1000).map(row => ({
          x: parseFloat(row.TotalPorcentajeAsistencia) || 0,
          y: parseFloat(row.PromedioFinalNumero) || 0
        })),
        backgroundColor: 'rgba(56, 189, 248, 0.6)',
        borderColor: 'rgba(56, 189, 248, 1)',
        pointRadius: 4,
        pointHoverRadius: 6
      }
    ]
  };

  const scatterOptions = {
    responsive: true,
    plugins: {
      legend: { display: false },
      title: { display: true, text: 'Asistencia vs Promedio Final (Muestra 1000 est.)' }
    },
    scales: {
      x: { title: { display: true, text: '% Asistencia' }, min: 0, max: 100 },
      y: { title: { display: true, text: 'Promedio Final' }, min: 0, max: 10 }
    }
  };

  // Preparar datos para Moodle Eventos
  const eventosCount = moodleData.reduce((acc, row) => {
    const evt = row.evento || 'Desconocido';
    acc[evt] = (acc[evt] || 0) + 1;
    return acc;
  }, {});

  const sortedEvents = Object.entries(eventosCount)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5); // Top 5

  const barData = {
    labels: sortedEvents.map(e => e[0]),
    datasets: [
      {
        label: 'Total de Interacciones',
        data: sortedEvents.map(e => e[1]),
        backgroundColor: 'rgba(168, 85, 247, 0.7)',
        borderColor: 'rgba(168, 85, 247, 1)',
        borderWidth: 1,
        borderRadius: 4
      }
    ]
  };

  const barOptions = {
    responsive: true,
    plugins: {
      legend: { display: false },
      title: { display: true, text: 'Top 5 Eventos en Moodle' }
    }
  };

  return (
    <div className="fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <header className="header">
        <div>
          <h1>
            <Users size={24} color="var(--text-accent)" style={{ marginRight: 10 }} />
            Análisis Automático: Cohorte 2025
          </h1>
          <p>
            Visualización directa y sin configuración de los datasets de SICOA y Moodle.
          </p>
        </div>
      </header>

      {/* Tarjetas de Resumen */}
      <div className="dashboard-grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))' }}>
        <div className="glass-panel stat-card">
          <div className="stat-icon" style={{ background: 'rgba(56, 189, 248, 0.1)' }}>
            <Users size={24} color="#38bdf8" />
          </div>
          <div className="stat-info">
            <span className="stat-label">Total Estudiantes SICOA</span>
            <span className="stat-value">{stats.totalStudents.toLocaleString()}</span>
          </div>
        </div>

        <div className="glass-panel stat-card">
          <div className="stat-icon" style={{ background: 'rgba(52, 211, 153, 0.1)' }}>
            <FileText size={24} color="#34d399" />
          </div>
          <div className="stat-info">
            <span className="stat-label">Promedio Global</span>
            <span className="stat-value">{stats.avgGrade}</span>
          </div>
        </div>

        <div className="glass-panel stat-card">
          <div className="stat-icon" style={{ background: 'rgba(251, 191, 36, 0.1)' }}>
            <Activity size={24} color="#fbbf24" />
          </div>
          <div className="stat-info">
            <span className="stat-label">Asistencia Promedio</span>
            <span className="stat-value">{stats.avgAttendance}%</span>
          </div>
        </div>

        <div className="glass-panel stat-card">
          <div className="stat-icon" style={{ background: 'rgba(168, 85, 247, 0.1)' }}>
            <BarChart2 size={24} color="#a855f7" />
          </div>
          <div className="stat-info">
            <span className="stat-label">Registros Moodle</span>
            <span className="stat-value">{stats.totalMoodleEvents.toLocaleString()}</span>
          </div>
        </div>
      </div>

      {/* Gráficos */}
      <div className="dashboard-grid">
        <div className="glass-panel chart-container">
          <Scatter options={scatterOptions} data={scatterData} />
        </div>
        <div className="glass-panel chart-container">
          <Bar options={barOptions} data={barData} />
        </div>
      </div>

      {/* Integración con el Panel de IA existente */}
      <div className="glass-panel">
        <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '1rem' }}>
          <Sparkles size={20} color="var(--status-yellow)" />
          Recomendaciones Estratégicas (Generadas por IA)
        </h3>
        <p style={{ color: 'var(--text-muted)', marginBottom: '1rem' }}>
          A continuación, el motor de IA analiza una muestra de los datos cargados automáticamente para generar un plan de acción.
        </p>
        
        {fusedSample && (
          <AIAnalysisPanel 
            mode="general"
            fusedData={fusedSample}
          />
        )}
      </div>

    </div>
  );
}
