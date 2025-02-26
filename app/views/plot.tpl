<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chart Viewer</title>
    <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
</head>
<body>
    <h1>SPC Real-Time Charts</h1>

    <div>
        <a href="/">Voltar para a Main Page</a><br><br>

        <button id="toggleNotifications" onclick="toggleNotifications()">Ativar Notificações</button>
    </div>

    <div>
        <h2>X Chart:</h2>
        <img id="mean_chart" src="" style="width: 100%; max-width: 600px;">

        <h2>R Chart:</h2>
        <img id="amplitude_chart" src="" style="width: 100%; max-width: 600px;">

        <h2>s Chart:</h2>
        <img id="stddev_chart" src="" style="width: 100%; max-width: 600px;">

        <h2>Individual Chart:</h2>
        <button id="toggleWEH" onclick="toggleWEH()">Ativar Limites da WEH</button><br>
        <img id="individual_chart" src="" style="width: 100%; max-width: 600px;">

        <h2>Moving Range Chart:</h2>
        <img id="moving_range_chart" src="" style="width: 100%; max-width: 600px;">
    </div>

    <script>
        const socket = io.connect("http://localhost:8080", { transports: ["websocket"] });

        socket.on('connect', () => console.log('Connected to WebSocket'));

        socket.on('chart_update', (data) => {
            updateChart("mean_chart", data.mean);
            updateChart("amplitude_chart", data.amplitude);
            updateChart("stddev_chart", data.stddev);
            updateChart("individual_chart", data.individual);
            updateChart("moving_range_chart", data.moving_range);
        });

        function updateChart(id, src) {
            document.getElementById(id).src = src;
        }

        function toggleNotifications() {
            fetch('/toggle_notifications')
                .then(response => response.json())
                .then(data => {
                    document.getElementById("toggleNotifications").innerText = 
                        data.status ? "Desativar Notificações" : "Ativar Notificações";
                })
                .catch(error => console.error("Erro ao alternar notificações:", error));
        }

        function toggleWEH() {
            fetch('/toggle_WEH')
                .then(response => response.json())
                .then(data => {
                    document.getElementById("toggleWEH").innerText = 
                        data.status ? "Desativar Limites da WEH" : "Ativar Limites da WEH";
                })
                .catch(error => console.error("Erro ao alternar WEH:", error));
        }

        function sendRandomData() {
            let newData = Array.from({ length: 5 }, () => Math.random() * 10);
            socket.emit('update_data', newData);
        }

        sendRandomData();   // Envia uma primeira amostra para evitar gráficos vazios

        setTimeout(() => {  // Aguarda 5 segundos antes de iniciar as simulações repetitivas
            setInterval(sendRandomData, 5000);
        }, 5000);
    </script>
</body>
</html>

