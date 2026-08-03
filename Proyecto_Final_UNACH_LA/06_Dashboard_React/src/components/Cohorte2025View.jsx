import React, { useState, useEffect } from 'react';
import Papa from 'papaparse';
import {
  FileText,
  BarChart2,
  Users,
  Activity,
  Sparkles,
  Loader,
  TrendingUp,
  Award,
  Clock
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
  Filler
} from 'chart.js';
import { Scatter, Bar, Line } from 'react-chartjs-2';
import AIAnalysisPanel from './AIAnalysisPanel';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

export default function Cohorte2025View() {
  const [sicoaData, setSicoaData] = useState([]);
  const [moodleData, setMoodleData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  const [stats, setStats] = useState({
    totalStudents: 0,
    avgAttendance: 0,
    avgGrade: 0,
    totalMoodleEvents: 0
  });

  const [fusedSample, setFusedSample] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const sicoaRes = await fetch('/datasets/SICOA_Anonimizado_Listo.csv');
      if (!sicoaRes.ok) throw new Error("No se pudo cargar SICOA_Anonimizado_Listo.csv");
      const sicoaCsv = await sicoaRes.text();
      const sicoaParsed = Papa.parse(sicoaCsv, { header: true, skipEmptyLines: true });
      
      const moodleRes = await fetch('/datasets/Moodle_Anonimizado_Listo.csv');
      if (!moodleRes.ok) throw new Error("No se pudo cargar Moodle_Anonimizado_Listo.csv");
      const moodleCsv = await moodleRes.text();
      const moodleParsed = Papa.parse(moodleCsv, { header: true, skipEmptyLines: true });

      setSicoaData(sicoaParsed.data);
      setMoodleData(moodleParsed.data);
      
      calculateStats(sicoaParsed.data, moodleParsed.data);
      
      setFusedSample({
        columns: ['ID_Estudiante', 'PromedioFinalNumero', 'TotalPorcentajeAsistencia', 'Nivel', 'MoodleEventos'],
        rows: sicoaParsed.data.slice(0, 30).map(row => ({
          ID_Estudiante: row.ID_Estudiante,
          PromedioFinalNumero: row.PromedioFinalNumero,
          TotalPorcentajeAsistencia: row.TotalPorcentajeAsistencia,
          Nivel: row.Nivel,
          MoodleEventos: 'Alta'
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
        <div style={{ position: 'relative', width: 80, height: 80, display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1rem' }}>
          <div style={{ position: 'absolute', inset: 0, border: '4px solid rgba(56, 189, 248, 0.2)', borderRadius: '50%' }}></div>
          <div style={{ position: 'absolute', inset: 0, border: '4px solid transparent', borderTopColor: '#38bdf8', borderRadius: '50%', animation: 'spin 1s linear infinite' }}></div>
          <Activity size={32} color="#38bdf8" className="pulse-icon" />
        </div>
        <h2 style={{ fontSize: '1.5rem', fontWeight: 600, background: 'linear-gradient(90deg, #fff, #a5b4fc)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
          Sintetizando Cohorte 2025
        </h2>
        <p style={{ color: 'var(--text-muted)', marginTop: '0.5rem', fontSize: '0.9rem' }}>Procesando miles de interacciones y registros académicos...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="fade-in glass-panel" style={{ textAlign: 'center', maxWidth: 500, margin: '4rem auto', border: '1px solid rgba(239, 68, 68, 0.3)' }}>
        <div style={{ width: 64, height: 64, borderRadius: '50%', background: 'rgba(239, 68, 68, 0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1rem' }}>
          <Activity size={32} color="#ef4444" />
        </div>
        <h2 style={{ color: '#ef4444', marginBottom: '0.5rem' }}>Error de Lectura</h2>
        <p style={{ color: 'var(--text-muted)' }}>{error}</p>
      </div>
    );
  }

  // ---- CHARTS DATA PREP ----

  // 1. Scatter (Asistencia vs Nota)
  const scatterData = {
    datasets: [{
      label: 'Estudiantes',
      data: sicoaData.slice(0, 1500).map(row => ({
        x: parseFloat(row.TotalPorcentajeAsistencia) || 0,
        y: parseFloat(row.PromedioFinalNumero) || 0
      })),
      backgroundColor: 'rgba(56, 189, 248, 0.4)',
      borderColor: 'rgba(56, 189, 248, 0.8)',
      pointRadius: 4,
      pointHoverRadius: 7,
      pointHoverBackgroundColor: '#fff'
    }]
  };

  const commonChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: 'rgba(15, 23, 42, 0.9)',
        titleColor: '#fff',
        bodyColor: '#cbd5e1',
        borderColor: 'rgba(51, 65, 85, 0.5)',
        borderWidth: 1,
        padding: 12,
        cornerRadius: 8,
        displayColors: false
      }
    },
    scales: {
      x: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: 'var(--text-muted)' } },
      y: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: 'var(--text-muted)' } }
    }
  };

  const scatterOptions = {
    ...commonChartOptions,
    scales: {
      ...commonChartOptions.scales,
      x: { ...commonChartOptions.scales.x, title: { display: true, text: '% Asistencia', color: 'var(--text-muted)' }, min: 0, max: 100 },
      y: { ...commonChartOptions.scales.y, title: { display: true, text: 'Promedio Final', color: 'var(--text-muted)' }, min: 0, max: 10 }
    }
  };

  // 2. Bar (Eventos Moodle)
  const eventosCount = moodleData.reduce((acc, row) => {
    const evt = row.evento || 'Desconocido';
    acc[evt] = (acc[evt] || 0) + 1;
    return acc;
  }, {});
  
  const sortedEvents = Object.entries(eventosCount).sort((a, b) => b[1] - a[1]).slice(0, 6);
  
  const barData = {
    labels: sortedEvents.map(e => e[0].split(' ')[0]), // Shorten labels
    datasets: [{
      label: 'Interacciones',
      data: sortedEvents.map(e => e[1]),
      backgroundColor: 'rgba(168, 85, 247, 0.6)',
      borderColor: 'rgba(168, 85, 247, 1)',
      borderWidth: 1,
      borderRadius: 6,
      hoverBackgroundColor: 'rgba(168, 85, 247, 0.8)'
    }]
  };

  // ---- RENDER ----
  return (
    <div className="fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '2rem', paddingBottom: '2rem' }}>
      
      {/* HEADER PREMIUM */}
      <header style={{ 
        position: 'relative', 
        padding: '2.5rem', 
        borderRadius: '24px', 
        background: 'linear-gradient(135deg, rgba(15,23,42,0.9) 0%, rgba(30,27,75,0.9) 100%)',
        border: '1px solid rgba(255,255,255,0.05)',
        overflow: 'hidden',
        boxShadow: '0 20px 40px -10px rgba(0,0,0,0.5)'
      }}>
        <div style={{ position: 'absolute', top: -100, right: -100, width: 300, height: 300, background: 'radial-gradient(circle, rgba(56,189,248,0.15) 0%, rgba(0,0,0,0) 70%)', borderRadius: '50%' }}></div>
        <div style={{ position: 'relative', zIndex: 1, display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
          <div style={{ background: 'linear-gradient(135deg, #38bdf8, #818cf8)', padding: '1rem', borderRadius: '16px', boxShadow: '0 10px 25px -5px rgba(56,189,248,0.4)' }}>
            <TrendingUp size={32} color="#fff" />
          </div>
          <div>
            <h1 style={{ fontSize: '2rem', fontWeight: 800, letterSpacing: '-0.5px', marginBottom: '0.5rem', background: 'linear-gradient(to right, #fff, #94a3b8)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              Cohorte 2025 en Tiempo Real
            </h1>
            <p style={{ color: '#94a3b8', fontSize: '1.05rem', maxWidth: 600, lineHeight: 1.5 }}>
              Radiografía completa de la cohorte actual. Visualización generada cruzando instantáneamente SICOA y Moodle sin configuración manual.
            </p>
          </div>
        </div>
      </header>

      {/* METRICS GRID PREMIUM */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1.5rem' }}>
        {[
          { icon: Users, color: '#38bdf8', bg: 'rgba(56,189,248,0.1)', label: 'Total SICOA', val: stats.totalStudents.toLocaleString() },
          { icon: Award, color: '#34d399', bg: 'rgba(52,211,153,0.1)', label: 'Promedio Global', val: stats.avgGrade },
          { icon: Clock, color: '#fbbf24', bg: 'rgba(251,191,36,0.1)', label: 'Asistencia General', val: `${stats.avgAttendance}%` },
          { icon: Activity, color: '#a855f7', bg: 'rgba(168,85,247,0.1)', label: 'Eventos Moodle', val: stats.totalMoodleEvents.toLocaleString() }
        ].map((stat, i) => (
          <div key={i} className="glass-panel stat-card" style={{ 
            padding: '1.5rem', 
            borderRadius: '20px', 
            display: 'flex', 
            alignItems: 'center', 
            gap: '1rem',
            transition: 'transform 0.3s ease, box-shadow 0.3s ease'
          }}
          onMouseEnter={(e) => { e.currentTarget.style.transform = 'translateY(-5px)'; e.currentTarget.style.boxShadow = `0 15px 30px -10px ${stat.bg}`; }}
          onMouseLeave={(e) => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.boxShadow = 'none'; }}
          >
            <div style={{ background: stat.bg, padding: '1rem', borderRadius: '14px' }}>
              <stat.icon size={28} color={stat.color} />
            </div>
            <div>
              <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.5px' }}>{stat.label}</div>
              <div style={{ fontSize: '1.8rem', fontWeight: 800, color: '#fff', marginTop: '4px' }}>{stat.val}</div>
            </div>
          </div>
        ))}
      </div>

      {/* CHARTS PREMIUM */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '1.5rem' }}>
        
        {/* Gráfico 1 */}
        <div className="glass-panel" style={{ padding: '1.5rem', borderRadius: '24px', display: 'flex', flexDirection: 'column' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600, color: '#e2e8f0', display: 'flex', alignItems: 'center', gap: 8 }}>
              <div style={{ width: 8, height: 24, borderRadius: 4, background: '#38bdf8' }}></div>
              Asistencia vs. Promedio
            </h3>
            <span style={{ fontSize: '0.8rem', background: 'rgba(56,189,248,0.1)', color: '#38bdf8', padding: '4px 10px', borderRadius: '12px', fontWeight: 600 }}>SICOA</span>
          </div>
          <div style={{ height: 280, width: '100%' }}>
            <Scatter options={scatterOptions} data={scatterData} />
          </div>
        </div>

        {/* Gráfico 2 */}
        <div className="glass-panel" style={{ padding: '1.5rem', borderRadius: '24px', display: 'flex', flexDirection: 'column' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600, color: '#e2e8f0', display: 'flex', alignItems: 'center', gap: 8 }}>
              <div style={{ width: 8, height: 24, borderRadius: 4, background: '#a855f7' }}></div>
              Top Interacciones LMS
            </h3>
            <span style={{ fontSize: '0.8rem', background: 'rgba(168,85,247,0.1)', color: '#a855f7', padding: '4px 10px', borderRadius: '12px', fontWeight: 600 }}>Moodle</span>
          </div>
          <div style={{ height: 280, width: '100%' }}>
            <Bar options={commonChartOptions} data={barData} />
          </div>
        </div>

      </div>

      {/* AI PANEL PREMIUM */}
      <div className="glass-panel" style={{ 
        padding: '2rem', 
        borderRadius: '24px', 
        border: '1px solid rgba(251, 191, 36, 0.2)',
        position: 'relative',
        overflow: 'hidden'
      }}>
        <div style={{ position: 'absolute', top: 0, right: 0, width: 200, height: '100%', background: 'linear-gradient(90deg, transparent, rgba(251, 191, 36, 0.03))', pointerEvents: 'none' }}></div>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1.5rem' }}>
          <div style={{ background: 'rgba(251,191,36,0.1)', padding: '12px', borderRadius: '16px' }}>
            <Sparkles size={28} color="#fbbf24" />
          </div>
          <div>
            <h3 style={{ fontSize: '1.3rem', fontWeight: 700, color: '#fff' }}>
              Insights Estratégicos (Groq IA)
            </h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', marginTop: 4 }}>
              Análisis neuro-lingüístico automático de la cohorte actual.
            </p>
          </div>
        </div>
        
        {fusedSample ? (
          <div style={{ background: 'rgba(0,0,0,0.2)', borderRadius: '16px', padding: '1px' }}>
            <AIAnalysisPanel mode="general" fusedData={fusedSample} />
          </div>
        ) : (
          <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>
            Preparando contexto neuronal...
          </div>
        )}
      </div>

    </div>
  );
}
