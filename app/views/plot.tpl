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

    <a href="/">Back to Home</a><br>

    <button id="toggleNotifications" onclick="toggleNotifications()">Desativar Notificações</button>

    <script>
        let notificationsEnabled = true;

        function toggleNotifications() {
            fetch('/toggle_notifications', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    notificationsEnabled = data.status;
                    document.getElementById("toggleNotifications").innerText = notificationsEnabled ? "Desativar Notificações" : "Ativar Notificações";
                })
                .catch(error => console.error("Erro ao alternar notificações:", error));
        }
    </script>

    <div>
        <h2>X Chart:</h2>
        <img id="mean_chart" src="" style="width: 100%; max-width: 600px;">
        <script>
            fetch('/plot/mean')
                .then(response => response.text())
                .then(data => {
                    document.getElementById("mean_chart").src = data;
                })
                .catch(error => console.error("Erro ao carregar a imagem:", error));
        </script>
    </div>

    <div>
        <h2>R Chart:</h2>
        <img id="amplitude_chart" src="" style="width: 100%; max-width: 600px;">
        <script>
            fetch('/plot/amplitude')
                .then(response => response.text())
                .then(data => {
                    document.getElementById("amplitude_chart").src = data;
                })
                .catch(error => console.error("Erro ao carregar a imagem:", error));
        </script>
    </div>

    <div>
        <h2>s Chart:</h2>
        <img id="stddev_chart" src="" style="width: 100%; max-width: 600px;">
        <script>
            fetch('/plot/stddev')
                .then(response => response.text())
                .then(data => {
                    document.getElementById("stddev_chart").src = data;
                })
                .catch(error => console.error("Erro ao carregar a imagem:", error));
        </script>
    </div>

    <div>
        <h2>Individual Chart:</h2>
        <img id="individual_chart" src="" style="width: 100%; max-width: 600px;">
        <script>
            fetch('/plot/individual')
                .then(response => response.text())
                .then(data => {
                    document.getElementById("individual_chart").src = data;
                })
                .catch(error => console.error("Erro ao carregar a imagem:", error));
        </script>
    </div>

    <div>
        <h2>Moving Range Chart:</h2>
        <img id="moving_range_chart" src="" style="width: 100%; max-width: 600px;">
        <script>
            fetch('/plot/moving_range')
                .then(response => response.text())
                .then(data => {
                    document.getElementById("moving_range_chart").src = data;
                })
                .catch(error => console.error("Erro ao carregar a imagem:", error));
        </script>
    </div>

    <script>
        const socket = io.connect("http://localhost:8080", { transports: ["websocket"] });

        socket.on('connect', () => {
            console.log('Connected to WebSocket');
        });

        socket.on('chart_update', (data) => {
            document.getElementById("mean_chart").src = data.mean;
            document.getElementById("amplitude_chart").src = data.amplitude;
            document.getElementById("stddev_chart").src = data.stddev;
            document.getElementById("individual_chart").src = data.individual;
            document.getElementById("moving_range_chart").src = data.moving_range;
        });

        function sendRandomData() {
            let newData = Array.from({ length: 5 }, () => Math.random() * 10);
            socket.emit('update_data', newData);
        }

        setInterval(sendRandomData, 5000); // Simulates new data every 5 seconds
    </script>
</body>
</html>

