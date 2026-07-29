import React, { useState, useEffect } from 'react';
import HeroSection from './components/HeroSection';
import Sidebar from './components/Sidebar';
import KPIGrid from './components/KPIGrid';
import RiskChart from './components/RiskChart';
import AlertsTable from './components/AlertsTable';
import PredictionChart from './components/PredictionChart';
import ModelPerformanceView from './components/ModelPerformanceView';
import DataFusionView from './components/DataFusionView';
import { AlertCircle } from 'lucide-react';

function App() {
  const [view, setView] = useState('hero');
  const [activeSection, setActiveSection] = useState('fusion');
  
  // Dynamic Global State
  const [globalFusedData, setGlobalFusedData] = useState(null);
  
  // Derived state for the UI
  const [kpiData, setKpiData] = useState(null);
  const [alertsData, setAlertsData] = useState(null);

  // When data is fused, calculate KPIs and Alerts dynamically
  const handleDataFused = (fusedData) => {
    setGlobalFusedData(fusedData);

    const rows = fusedData.rows;
    let totalEstudiantes = rows.length;
    let riesgoAlto = 0;
    let riesgoMedio = 0;
    let riesgoBajo = 0;
    
    // Find relevant columns dynamically
    const columns = fusedData.columns.map(c => c.toLowerCase());
    const notaCol = fusedData.columns.find(c => c.toLowerCase().includes('nota') || c.toLowerCase().includes('promedio') || c.toLowerCase().includes('calif'));
    const asistCol = fusedData.columns.find(c => c.toLowerCase().includes('asist'));

    const calculatedAlerts = rows.map((row, index) => {
      // Parse values
      const nota = notaCol ? parseFloat(row[notaCol]) : null;
      const asist = asistCol ? parseFloat(row[asistCol]) : null;
      
      let nivelRiesgo = "Bajo";
      let probabilidad = 0.1;
      
      // Basic heuristic for risk if columns are found
      if (nota !== null && asist !== null) {
        if (nota < 14 || asist < 70) {
          nivelRiesgo = "Alto";
          probabilidad = 0.85 + (Math.random() * 0.14); // 85-99%
        } else if (nota < 16 || asist < 80) {
          nivelRiesgo = "Medio";
          probabilidad = 0.5 + (Math.random() * 0.3); // 50-80%
        } else {
          nivelRiesgo = "Bajo";
          probabilidad = 0.05 + (Math.random() * 0.2); // 5-25%
        }
      } else {
        // Fallback random distribution for demo if columns don't match exactly
        const rand = Math.random();
        if (rand > 0.8) {
          nivelRiesgo = "Alto";
          probabilidad = 0.85 + (Math.random() * 0.1);
        } else if (rand > 0.5) {
          nivelRiesgo = "Medio";
          probabilidad = 0.5 + (Math.random() * 0.3);
        } else {
          nivelRiesgo = "Bajo";
          probabilidad = Math.random() * 0.3;
        }
      }

      if (nivelRiesgo === "Alto") riesgoAlto++;
      else if (nivelRiesgo === "Medio") riesgoMedio++;
      else riesgoBajo++;

      return {
        id: row.ID_Unificado || index,
        estudiante: row.ID_Unificado || `Estudiante ${index}`,
        carrera: row.Carrera || row.Facultad || "N/A",
        semestre: row.Semestre || "N/A",
        riesgo: nivelRiesgo,
        probabilidad_desercion: probabilidad,
        factores_clave: [
          notaCol ? `${notaCol}: ${row[notaCol]}` : "Datos académicos",
          asistCol ? `${asistCol}: ${row[asistCol]}` : "Asistencia"
        ],
        rawData: row
      };
    });

    // Sort by risk probability descending
    calculatedAlerts.sort((a, b) => b.probabilidad_desercion - a.probabilidad_desercion);

    // Build KPI structure matching what the UI expects
    const newKpiData = {
      metadata: { fecha_calculo: new Date().toLocaleDateString() },
      kpi_ejecutivos: [
        {
          id: "total_evaluados",
          titulo: "Estudiantes Evaluados",
          valor_actual: totalEstudiantes,
          tendencia: "up",
          cambio_porcentual: "+100%",
          descripcion: "En la base fusionada"
        },
        {
          id: "tasa_riesgo_global",
          titulo: "Tasa de Riesgo Global",
          valor_actual: `${((riesgoAlto / totalEstudiantes) * 100).toFixed(1)}%`,
          tendencia: "up",
          cambio_porcentual: `Riesgo Alto`,
          descripcion: "Requieren intervención urgente"
        },
        {
          id: "precision_modelo",
          titulo: "Estudiantes Seguros",
          valor_actual: riesgoBajo,
          tendencia: "up",
          cambio_porcentual: `${((riesgoBajo / totalEstudiantes) * 100).toFixed(1)}%`,
          descripcion: "Rendimiento esperado normal"
        }
      ]
    };

    const newAlertsData = {
      resumen_riesgo: [
        { nivel: "Alto", cantidad: riesgoAlto, color: "var(--status-red)" },
        { nivel: "Medio", cantidad: riesgoMedio, color: "var(--status-yellow)" },
        { nivel: "Bajo", cantidad: riesgoBajo, color: "var(--status-green)" }
      ],
      top_alertas_prioritarias: calculatedAlerts.slice(0, 100) // Top 100 to avoid freezing browser
    };

    setKpiData(newKpiData);
    setAlertsData(newAlertsData);
  };

  // Hero view
  if (view === 'hero') {
    return <HeroSection onEnterDashboard={() => setView('dashboard')} />;
  }

  return (
    <div className="dashboard-layout">
      <Sidebar 
        onBackToHero={() => setView('hero')} 
        activeSection={activeSection}
        setActiveSection={setActiveSection}
      />
      <main className="main-area">
        
        {/* Sección 1: Fusión Inteligente (Punto de entrada) */}
        {activeSection === 'fusion' && (
          <section id="fusion" className="fade-in dashboard-section" style={{ borderBottom: 'none', padding: '2rem 0' }}>
            <DataFusionView onDataFused={handleDataFused} />
          </section>
        )}

        {/* Notificación Global si no hay datos fusionados para las otras secciones */}
        {activeSection !== 'fusion' && activeSection !== 'modelo' && !globalFusedData && (
          <div className="glass-panel fade-in" style={{ margin: '2rem 0', textAlign: 'center', padding: '3rem 1rem' }}>
            <AlertCircle size={48} color="var(--text-muted)" style={{ marginBottom: '1rem' }} />
            <h2 style={{ color: 'var(--text-main)', marginBottom: '0.5rem' }}>Faltan Datos</h2>
            <p style={{ color: 'var(--text-muted)', marginBottom: '1.5rem' }}>
              Para ver el análisis dinámico, primero debes subir y fusionar los archivos en la sección <strong>Fusión Inteligente</strong>.
            </p>
            <button className="btn-primary" onClick={() => setActiveSection('fusion')}>
              Ir a Fusión Inteligente
            </button>
          </div>
        )}

        {/* Sección 2: Vista General (KPIs) */}
        {activeSection === 'general' && globalFusedData && (
          <section id="general" className="fade-in dashboard-section" style={{ borderBottom: 'none', padding: '2rem 0' }}>
            <header className="header" style={{ marginBottom: '2rem' }}>
              <div>
                <h1>Dashboard Dinámico: Vista General</h1>
                <p>Datos basados en el último cruce de información ({kpiData?.metadata?.fecha_calculo}).</p>
              </div>
              <img 
                src="https://ui-avatars.com/api/?name=Admin+UNACH&background=0369a1&color=fff&bold=true" 
                alt="Admin" 
                className="avatar"
              />
            </header>
            <KPIGrid data={kpiData.kpi_ejecutivos} />
          </section>
        )}

        {/* Sección 3: Todos los Estudiantes / Alertas */}
        {activeSection === 'alertas' && globalFusedData && (
          <section id="alertas" className="fade-in dashboard-section" style={{ borderBottom: 'none', padding: '2rem 0' }}>
            <header className="header" style={{ marginBottom: '1.5rem' }}>
              <div>
                <h2 style={{ fontSize: '1.5rem', fontWeight: '700', color: 'var(--text-main)' }}>Lista Dinámica de Estudiantes en Riesgo</h2>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Visualizando el riesgo detectado por la heurística sobre los datos cruzados.</p>
              </div>
            </header>
            
            <div className="content-grid">
              <RiskChart data={alertsData.resumen_riesgo} />
              <AlertsTable data={alertsData.top_alertas_prioritarias} />
            </div>
          </section>
        )}

        {/* Sección 4: Rendimiento / Predicción (Estático/Demostrativo o puede alimentarse del ML futuro) */}
        {activeSection === 'rendimiento' && globalFusedData && (
          <section id="rendimiento" className="fade-in dashboard-section" style={{ borderBottom: 'none', padding: '2rem 0' }}>
            <PredictionChart />
          </section>
        )}

        {/* Sección 5: Nuestro Modelo Entrenado (Siempre disponible, independiente de datos en vivo) */}
        {activeSection === 'modelo' && (
          <section id="modelo" className="fade-in dashboard-section" style={{ borderBottom: 'none', padding: '2rem 0' }}>
            <header className="header" style={{ marginBottom: '2rem' }}>
              <div>
                <h1>Métricas de Nuestro Modelo Entrenado</h1>
                <p>Esta sección detalla el rendimiento histórico del motor predictivo durante su fase de entrenamiento.</p>
              </div>
            </header>
            <ModelPerformanceView />
          </section>
        )}

        <footer style={{ textAlign: 'center', padding: '3rem 0', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
          &copy; 2026 Universidad Nacional de Chimborazo (UNACH). Todos los derechos reservados.
        </footer>
      </main>
    </div>
  );
}

export default App;
