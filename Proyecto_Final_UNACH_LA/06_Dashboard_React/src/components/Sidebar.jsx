import React from 'react';
import { LayoutDashboard, AlertTriangle, TrendingUp, BrainCircuit } from 'lucide-react';

export default function Sidebar() {
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
        <div className="nav-item active">
          <LayoutDashboard size={20} />
          <span>Vista General</span>
        </div>
        <div className="nav-item">
          <AlertTriangle size={20} />
          <span>Alertas Críticas</span>
        </div>
        <div className="nav-item">
          <TrendingUp size={20} />
          <span>Rendimiento</span>
        </div>
        <div className="nav-item">
          <BrainCircuit size={20} />
          <span>Motor ML</span>
        </div>
      </nav>

      <div className="system-status">
        <div className="pulse"></div>
        <span>Motor ML Activo</span>
      </div>
    </aside>
  );
}
