import React, { useState, useEffect } from 'react';
import {
  LayoutDashboard,
  Users,
  TrendingUp,
  BrainCircuit,
  FileUp,
  Link2,
  ArrowLeft,
  GraduationCap,
  Activity
} from 'lucide-react';

export default function Sidebar({ onBackToHero, activeSection, setActiveSection }) {
  const navItems = [
    { id: 'general', icon: LayoutDashboard, label: 'Vista General' },
    { id: 'alertas', icon: Users, label: 'Todos los Estudiantes' },
    { id: 'rendimiento', icon: TrendingUp, label: 'Predicción Temporal' },
    { id: 'modelo', icon: Activity, label: 'Rendimiento ML' },
    { id: 'import', icon: FileUp, label: 'Analista IA (Groq)' },
    { id: 'motor', icon: BrainCircuit, label: 'Motor ML' },
    { id: 'integraciones', icon: Link2, label: 'Integraciones' },
  ];

  return (
    <aside className="sidebar">
      <div className="logo-area">
        <div className="logo-icon">
          <GraduationCap size={22} color="white" />
        </div>
        <div className="logo-text">
          <h2>UNACH-LA</h2>
          <p>Learning Analytics</p>
        </div>
      </div>

      <nav className="nav-links">
        <button className="sidebar-back-btn" onClick={onBackToHero}>
          <ArrowLeft size={16} />
          Volver al Inicio
        </button>

        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <div
              key={item.id}
              className={`nav-item ${activeSection === item.id ? 'active' : ''}`}
              onClick={() => setActiveSection(item.id)}
            >
              <Icon size={18} />
              <span>{item.label}</span>
            </div>
          );
        })}
      </nav>

      <div className="system-status">
        <div className="pulse" />
        <span>Motor ML Activo • Groq IA</span>
      </div>
    </aside>
  );
}
