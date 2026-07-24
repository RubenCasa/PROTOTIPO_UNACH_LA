import React from 'react';
import AlertsTable from './AlertsTable';
import { AlertTriangle } from 'lucide-react';

export default function AlertasView({ data }) {
  // En una vista completa mostramos más alertas, por ejemplo 50 o todas.
  // Aquí usaremos los datos completos pasados por prop.
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      <div className="header">
        <div>
          <h1 style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <AlertTriangle color="var(--status-red)" />
            Centro de Alertas Críticas
          </h1>
          <p>Listado completo de estudiantes detectados por el modelo predictivo XGBoost.</p>
        </div>
      </div>
      
      {/* Reutilizamos el componente AlertsTable pero le podríamos pasar data completa */}
      <AlertsTable data={data} />
    </div>
  );
}
