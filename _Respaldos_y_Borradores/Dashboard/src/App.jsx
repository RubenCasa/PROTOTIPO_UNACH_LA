import React, { useState, useEffect } from 'react';
import { Activity, BookOpen, AlertTriangle, CheckCircle, Brain, Users } from 'lucide-react';
import kpiData from './data/kpis_academicos.json';
import mlData from './data/resultados_ml.json';
import alertsData from './data/alertas_unach_la.json';
import KPICards from './components/KPICards';
import MLMetrics from './components/MLMetrics';
import AlertsTable from './components/AlertsTable';

function App() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate loading data to show off some animations
    setTimeout(() => setLoading(false), 800);
  }, []);

  if (loading) {
    return (
      <div className="dashboard-container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <div className="glass-card animate-fade-in" style={{ textAlign: 'center' }}>
          <Activity size={48} color="#3b82f6" className="animate-pulse" />
          <h2 style={{ marginTop: '1rem' }}>Cargando Motor UNACH-LA...</h2>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <header className="animate-fade-in">
        <h1>UNACH-LA Analytics</h1>
        <p className="subtitle">
          Sistema Inteligente de Alerta Temprana y Diagnóstico Académico
        </p>
      </header>

      <main>
        {/* KPI Section */}
        <section className="animate-fade-in delay-1">
          <KPICards data={kpiData.kpi_ejecutivos} />
        </section>

        {/* Main Grid: ML Results + Alerts */}
        <div className="main-grid">
          <section className="animate-fade-in delay-2">
            <AlertsTable alerts={alertsData.top_alertas_prioritarias} />
          </section>

          <section className="animate-fade-in delay-3">
            <MLMetrics mlData={mlData} />
          </section>
        </div>
      </main>
    </div>
  );
}

export default App;
