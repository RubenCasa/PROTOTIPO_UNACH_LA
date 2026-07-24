import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import KPIGrid from './components/KPIGrid';
import RiskChart from './components/RiskChart';
import AlertsTable from './components/AlertsTable';

function App() {
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

  if (loading) {
    return <div className="loading-state">Cargando Motor Predictivo UNACH-LA...</div>;
  }

  if (error) {
    return (
      <div className="loading-state" style={{ color: 'var(--status-red)', flexDirection: 'column', gap: '1rem' }}>
        <p>⚠️ Error Crítico</p>
        <p style={{ fontSize: '1rem', color: 'var(--text-muted)' }}>{error}</p>
      </div>
    );
  }

  return (
    <div className="dashboard-layout">
      <Sidebar />
      <main className="main-area">
        <header className="header">
          <div>
            <h1>Dashboard Institucional</h1>
            <p>Última actualización: {kpiData.metadata.fecha_calculo}</p>
          </div>
          <img 
            src="https://ui-avatars.com/api/?name=Admin+UNACH&background=0D8ABC&color=fff" 
            alt="Admin" 
            className="avatar"
          />
        </header>

        <section>
          <KPIGrid data={kpiData.kpi_ejecutivos} />
        </section>

        <section className="content-grid">
          <RiskChart data={alertsData.resumen_riesgo} />
          <AlertsTable data={alertsData.top_alertas_prioritarias} />
        </section>
      </main>
    </div>
  );
}

export default App;
