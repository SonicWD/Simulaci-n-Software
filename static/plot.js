document.addEventListener('DOMContentLoaded', function() {
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            let trace1 = {
                x: data.llegadas,
                y: data.tiempos_ciclo,
                mode: 'markers',
                type: 'scatter',
                name: 'Tiempo de Ciclo'
            };

            let layout = {
                title: 'Tiempos de Ciclo de las Tareas',
                xaxis: {
                    title: 'Tiempo de Llegada (minutos)'
                },
                yaxis: {
                    title: 'Tiempo de Ciclo (minutos)'
                }
            };

            let plotData = [trace1];
            Plotly.newPlot('graph', plotData, layout);
        });
});
