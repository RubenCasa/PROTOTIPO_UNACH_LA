document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Fetch data
        const kpisRes = await fetch('../03_Visualizacion_y_KPIs/kpis_academicos.json');
        const kpisData = await kpisRes.json();
        
        const alertasRes = await fetch('../04_Prototipo_UNACH_LA/alertas_unach_la.json');
        const alertasData = await alertasRes.json();

        // Update header
        document.getElementById('fecha-calculo').textContent = `Última actualización: ${kpisData.metadata.fecha_calculo}`;

        // Render KPIs
        renderKPIs(kpisData.kpi_ejecutivos);

        // Render Alerts Table
        renderAlertsTable(alertasData.top_alertas_prioritarias);

        // Render Chart
        renderChart(alertasData.resumen_riesgo);

    } catch (error) {
        console.error("Error loading data:", error);
        document.getElementById('kpi-container').innerHTML = `
            <div class="kpi-card" style="border-color: var(--status-red)">
                <h3 style="color: var(--status-red)">Error de conexión</h3>
                <p style="font-size: 0.9rem; margin-top: 10px; color: var(--text-muted)">
                    Asegúrate de estar ejecutando el dashboard a través de un servidor local (ej. python -m http.server) 
                    y no directamente abriendo el archivo HTML, para evitar políticas de CORS.
                </p>
            </div>
        `;
    }
});

function renderKPIs(kpis) {
    const container = document.getElementById('kpi-container');
    container.innerHTML = '';

    const icons = {
        'KPI_01_Tasa_Riesgo_Academico': '📉',
        'KPI_02_Promedio_General_Notas': '📈',
        'KPI_03_Asistencia_Promedio': '👥',
        'KPI_04_Efectividad_Modelo_ML': '🤖'
    };

    for (const [key, kpi] of Object.entries(kpis)) {
        const icon = icons[key] || '📌';
        const card = document.createElement('div');
        card.className = 'kpi-card';
        
        card.innerHTML = `
            <div class="kpi-title">
                <span>${kpi.nombre}</span>
                <span>${icon}</span>
            </div>
            <div class="kpi-value">
                ${kpi.valor} <span class="kpi-unit">${kpi.unidad}</span>
            </div>
            <div class="kpi-meta">
                <span>Meta: ${kpi.meta_institucional}</span>
                <span class="status-badge status-${kpi.estado}">${kpi.estado}</span>
            </div>
        `;
        container.appendChild(card);
    }
}

function renderAlertsTable(alertas) {
    const tbody = document.querySelector('#alerts-table tbody');
    tbody.innerHTML = '';

    // Show top 15 alerts for brevity
    const topAlertas = alertas.slice(0, 15);

    topAlertas.forEach(alerta => {
        const tr = document.createElement('tr');
        
        let colorRiesgo = 'var(--status-green)';
        if (alerta.nivel_riesgo === 'ALTO') colorRiesgo = 'var(--status-red)';
        if (alerta.nivel_riesgo === 'MEDIO') colorRiesgo = 'var(--status-yellow)';

        tr.innerHTML = `
            <td>
                <strong>${alerta.id_estudiante}</strong><br>
                <span style="font-size: 0.75rem; color: var(--text-muted)">${alerta.carrera}</span>
            </td>
            <td>
                ${alerta.probabilidad_riesgo_ml}%
                <div class="riesgo-bar">
                    <div class="riesgo-fill" style="width: ${alerta.probabilidad_riesgo_ml}%; background-color: ${colorRiesgo}"></div>
                </div>
            </td>
            <td>
                <span class="status-badge status-${alerta.nivel_riesgo === 'ALTO' ? 'CRÍTICO' : (alerta.nivel_riesgo === 'MEDIO' ? 'ADVERTENCIA' : 'ÓPTIMO')}">
                    ${alerta.semaforo.split(' ')[0]}
                </span>
            </td>
            <td style="font-size: 0.8rem; max-width: 200px;">
                ${alerta.accion_recomendada}
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function renderChart(resumen) {
    const ctx = document.getElementById('riesgoChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Alto Riesgo', 'Riesgo Medio', 'Bajo Riesgo'],
            datasets: [{
                data: [resumen.alto, resumen.medio, resumen.bajo],
                backgroundColor: [
                    'rgba(239, 68, 68, 0.8)',
                    'rgba(245, 158, 11, 0.8)',
                    'rgba(16, 185, 129, 0.8)'
                ],
                borderColor: [
                    'rgba(239, 68, 68, 1)',
                    'rgba(245, 158, 11, 1)',
                    'rgba(16, 185, 129, 1)'
                ],
                borderWidth: 1,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '70%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#94a3b8',
                        padding: 20,
                        font: {
                            family: 'Inter',
                            size: 12
                        }
                    }
                }
            }
        }
    });
}
