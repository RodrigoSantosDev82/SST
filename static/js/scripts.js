window.onload = function() {
    try {
        var expiradoCount = JSON.parse(document.getElementById('expirado_count').textContent);
        var proximoCount = JSON.parse(document.getElementById('proximo_count').textContent);
        var validoCount = JSON.parse(document.getElementById('valido_count').textContent);

        var ctx = document.getElementById('certificadosChart').getContext('2d');
        var certificadosChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Expirado', 'Próximo a Vencer', 'Válido'],
                datasets: [{
                    label: 'Contagem de Certificados',
                    data: [expiradoCount, proximoCount, validoCount],
                    backgroundColor: ['#f8d7da', '#fff3cd', '#d4edda'],
                    borderColor: ['#721c24', '#856404', '#155724'],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    } catch (e) {
        console.error('Erro ao carregar dados para o gráfico:', e);
    }
}
