import React, { useState, useEffect } from 'react';
import HeroSection from './components/HeroSection';
import Sidebar from './components/Sidebar';
import KPIGrid from './components/KPIGrid';
import RiskChart from './components/RiskChart';
import AlertsTable from './components/AlertsTable';
import PredictionChart from './components/PredictionChart';
import MotorMLView from './components/MotorMLView';
import ModelPerformanceView from './components/ModelPerformanceView';
import ImportExportView from './components/ImportExportView';
import IntegrationsView from './components/IntegrationsView';

function App() {
  const [view, setView] = useState('hero'); // 'hero' | 'dashboard'
  const [activeSection, setActiveSection] = useState('general');
  const [kpiData, setKpiData] = useState(null);
  const [alertsData, setAlertsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [kpisRes, alertsRes] = await Promise.all([
          fetch('/data/kpis_academicos.json'),
          fetch('/data/alertas_unach_la.json')
        ]);
        
        if (!kpisRes.ok || !alertsRes.ok) {
          throw new Error('Fallo al cargar los datos. Revisa la ruta en public/data.');
        }

        const kpis = await kpisRes.json();
        const alerts = await alertsRes.json();

        setKpiData(kpis);
        setAlertsData(alerts);
        setLoading(false);
      } catch (err) {
        console.error(err);
        setError(err.message);
        setLoading(false);
      }
    };

    loadData();
  }, []);

  // Hero view
  if (view === 'hero') {
    return <HeroSection onEnterDashboard={() => setView('dashboard')} />;
  }

  // Loading
  if (loading) {
    return (
      <div className="loading-state">
        <div className="spinner" />
        Cargando Motor Predictivo UNACH-LA...
      </div>
    );
  }

  // Error
  if (error) {
    return (
      <div className="loading-state" style={{ color: 'var(--status-red)', flexDirection: 'column', gap: '1rem' }}>
        <p>⚠️ Error Crítico</p>
        <p style={{ fontSize: '0.95rem', color: 'var(--text-muted)' }}>{error}</p>
      </div>
    );
  }

  return (
    <div className="dashboard-layout">
      <Sidebar 
        onBackToHero={() => setView('hero')} 
        activeSection={activeSection}
        setActiveSection={setActiveSection}
      />
      <main className="main-area">
        
        {/* Sección 1: Vista General (KPIs) */}
        {activeSection === 'general' && (
          <section id="general" className="fade-in dashboard-section" style={{ borderBottom: 'none', padding: '2rem 0' }}>
            <header className="header" style={{ marginBottom: '2rem' }}>
              <div>
                <h1>Dashboard Institucional All-in-One</h1>
                <p>Última actualización: {kpiData.metadata.fecha_calculo}</p>
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

        {/* Sección 2: Todos los Estudiantes / Alertas */}
        {activeSection === 'alertas' && (
          <section id="alertas" className="fade-in dashboard-section" style={{ borderBottom: 'none', padding: '2rem 0' }}>
            <header className="header" style={{ marginBottom: '1.5rem' }}>
              <div>
                <h2 style={{ fontSize: '1.5rem', fontWeight: '700', color: 'var(--text-main)' }}>Lista General de Estudiantes (Riesgo ML)</h2>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Visualizando todos los estudiantes evaluados por el motor predictivo.</p>
              </div>
            </header>
            
            <div className="content-grid">
              <RiskChart data={alertsData.resumen_riesgo} />
              {/* The AlertsTable now represents ALL students */}
              <AlertsTable data={alertsData.top_alertas_prioritarias} />
            </div>
          </section>
        )}

        {/* Sección 3: Rendimiento / Predicción */}
        {activeSection === 'rendimiento' && (
          <section id="rendimiento" className="fade-in dashboard-section" style={{ borderBottom: 'none', padding: '2rem 0' }}>
            <PredictionChart />
          </section>
        )}

        {/* Sección 4: Rendimiento del Modelo ML */}
        {activeSection === 'modelo' && (
          <section id="modelo" className="fade-in dashboard-section" style={{ borderBottom: 'none', padding: '2rem 0' }}>
            <ModelPerformanceView />
          </section>
        )}

        {/* Sección 5: Importación / IA (Groq) */}
        {activeSection === 'import' && (
          <section id="import" className="fade-in dashboard-section" style={{ borderBottom: 'none', padding: '2rem 0' }}>
            <ImportExportView />
          </section>
        )}

        {/* Sección 6: Motor ML (SICOA) */}
        {activeSection === 'motor' && (
          <section id="motor" className="fade-in dashboard-section" style={{ borderBottom: 'none', padding: '2rem 0' }}>
            <MotorMLView />
          </section>
        )}

        {/* Sección 7: Integraciones */}
        {activeSection === 'integraciones' && (
          <section id="integraciones" className="fade-in dashboard-section" style={{ borderBottom: 'none', padding: '2rem 0' }}>
            <IntegrationsView />
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
