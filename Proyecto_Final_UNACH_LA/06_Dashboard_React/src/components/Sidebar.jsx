import React from 'react';
import { LayoutDashboard, AlertTriangle, TrendingUp, BrainCircuit } from 'lucide-react';

export default function Sidebar({ activeTab, onTabChange }) {
  return (
    <aside className="sidebar">
      <div className="logo-area">
        <div className="logo-icon"></div>
        <div className="logo-text">
          <h2>UNACH-LA</h2>
          <p>Learning Analytics</p>
        </div>
      </div>

      <nav className="nav-links">
        <div 
          className={`nav-item ${activeTab === 'general' ? 'active' : ''}`}
          onClick={() => onTabChange('general')}
        >
          <LayoutDashboard size={20} />
          <span>Vista General</span>
        </div>
        <div 
          className={`nav-item ${activeTab === 'alertas' ? 'active' : ''}`}
          onClick={() => onTabChange('alertas')}
        >
          <AlertTriangle size={20} />
          <span>Alertas Críticas</span>
        </div>
        <div 
          className={`nav-item ${activeTab === 'rendimiento' ? 'active' : ''}`}
          onClick={() => onTabChange('rendimiento')}
        >
          <TrendingUp size={20} />
          <span>Rendimiento</span>
        </div>
        <div 
          className={`nav-item ${activeTab === 'motor' ? 'active' : ''}`}
          onClick={() => onTabChange('motor')}
        >
          <BrainCircuit size={20} />
          <span>Motor ML (SICOA)</span>
        </div>
      </nav>

      <div className="system-status">
        <div className="pulse"></div>
        <span>Motor ML Activo</span>
      </div>
    </aside>
  );
}
