document.addEventListener('DOMContentLoaded', function() {
    // Event listener para el botón que inicia la simulación
    document.getElementById('startSimulationButton').addEventListener('click', function() {
        // Obtener los parámetros de simulación del formulario
        let params = {
            TIEMPO_LLEGADA_TAREAS: parseInt(document.getElementById('TIEMPO_LLEGADA_TAREAS').value),
            TIEMPO_PLANIFICACION: parseInt(document.getElementById('TIEMPO_PLANIFICACION').value),
            TIEMPO_DESARROLLO_MIN: parseInt(document.getElementById('TIEMPO_DESARROLLO_MIN').value),
            TIEMPO_DESARROLLO_MAX: parseInt(document.getElementById('TIEMPO_DESARROLLO_MAX').value),
            TIEMPO_REVISION: parseInt(document.getElementById('TIEMPO_REVISION').value),
            TIEMPO_PRUEBAS_MIN: parseInt(document.getElementById('TIEMPO_PRUEBAS_MIN').value),
            TIEMPO_PRUEBAS_MAX: parseInt(document.getElementById('TIEMPO_PRUEBAS_MAX').value),
            TIEMPO_DESPLIEGUE: parseInt(document.getElementById('TIEMPO_DESPLIEGUE').value),
            DURACION_SIMULACION: parseInt(document.getElementById('DURACION_SIMULACION').value)
        };

        // Enviar los parámetros al servidor Flask
        fetch('/data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        })
        .then(response => response.json())
        .then(data => {
            // Configurar el gráfico Plotly con los datos recibidos
            let trace1 = {
                x: data.llegadas,
                y: data.tiempos_ciclo,
                mode: 'markers',
                type: 'scatter',
                name: 'Tiempo de Ciclo',
                marker: { color: 'rgba(31, 119, 180, 0.8)', size: 8 }
            };

            let layout = {
                title: 'Tiempos de Ciclo de las Tareas',
                xaxis: {
                    title: 'Tiempo de Llegada (minutos)',
                    showgrid: true,
                    zeroline: false
                },
                yaxis: {
                    title: 'Tiempo de Ciclo (minutos)',
                    showline: false
                },
                plot_bgcolor: '#f4f4f4',
                paper_bgcolor: '#f4f4f4'
            };

            let plotData = [trace1];
            Plotly.newPlot('graph', plotData, layout);
        })
        .catch(error => console.error('Error fetching data:', error));
    });
});
