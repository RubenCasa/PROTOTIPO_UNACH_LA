import React, { useState, useEffect, useRef } from 'react';
import { ArrowRight, GraduationCap, Sparkles, Shield, Cpu } from 'lucide-react';

function useCountUp(end, duration = 2000, start = 0) {
  const [count, setCount] = useState(start);
  const [hasStarted, setHasStarted] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !hasStarted) {
          setHasStarted(true);
        }
      },
      { threshold: 0.3 }
    );
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, [hasStarted]);

  useEffect(() => {
    if (!hasStarted) return;
    const startTime = Date.now();
    const timer = setInterval(() => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      // Ease out quad
      const eased = 1 - (1 - progress) * (1 - progress);
      setCount(Math.floor(start + (end - start) * eased));
      if (progress >= 1) clearInterval(timer);
    }, 16);
    return () => clearInterval(timer);
  }, [hasStarted, end, duration, start]);

  return [count, ref];
}

export default function HeroSection({ onEnterDashboard }) {
  const [count4000, ref1] = useCountUp(4000, 2500);
  const [countML, ref2] = useCountUp(30, 2000);
  const [countAlerts, ref3] = useCountUp(1831, 2200);

  return (
    <div className="hero-container">
      {/* Background image */}
      <img
        src="/unach_hero.png"
        alt="Campus Universidad Nacional de Chimborazo"
        className="hero-bg-image"
      />

      {/* Dark overlay */}
      <div className="hero-overlay" />

      {/* Floating particles */}
      <div className="hero-particles">
        {Array.from({ length: 8 }).map((_, i) => (
          <div key={i} className="particle" />
        ))}
      </div>

      {/* Content */}
      <div className="hero-content">
        <div className="hero-badge">
          <div className="dot" />
          <span>Sistema Activo — Motor Predictivo XGBoost v2.0</span>
        </div>

        <h1 className="hero-title">
          <span className="gradient-text">Universidad Nacional</span>
          <br />
          de Chimborazo
        </h1>

        <p className="hero-subtitle">
          Sistema de Alerta Temprana con Inteligencia Artificial.
          Predicción de riesgo académico, análisis de datos y
          planes de intervención personalizados para cada estudiante.
        </p>

        <div className="hero-stats">
          <div className="hero-stat" ref={ref1}>
            <div className="hero-stat-value">{count4000.toLocaleString()}</div>
            <div className="hero-stat-label">Estudiantes Evaluados</div>
          </div>
          <div className="hero-stat" ref={ref2}>
            <div className="hero-stat-value">{countML}</div>
            <div className="hero-stat-label">Features Optimizadas</div>
          </div>
          <div className="hero-stat" ref={ref3}>
            <div className="hero-stat-value">{countAlerts.toLocaleString()}</div>
            <div className="hero-stat-label">Alertas Generadas</div>
          </div>
        </div>

        <button className="hero-cta" onClick={onEnterDashboard}>
          <GraduationCap size={22} />
          Acceder al Dashboard
          <ArrowRight size={18} />
        </button>

        <div className="hero-tags">
          <span className="hero-tag">
            <Sparkles size={14} /> IA Groq — Llama 3.3
          </span>
          <span className="hero-tag">
            <Shield size={14} /> SICOA Integrado
          </span>
          <span className="hero-tag">
            <Cpu size={14} /> Motor XGBoost
          </span>
          <span className="hero-tag">
            <GraduationCap size={14} /> Moodle LMS
          </span>
        </div>
      </div>
    </div>
  );
}
