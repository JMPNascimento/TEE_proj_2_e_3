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
        <h2>X Chart</h2>
        <img id="mean_chart" src="{{ chart_url }}" style="width: 100%; max-width: 600px;">
    </div>

    <div>
        <h2>R Chart</h2>
        <img id="amplitude_chart" src="/plot/amplitude" style="width: 100%; max-width: 600px;">
    </div>

    <div>
        <h2>s Chart</h2>
        <img id="stddev_chart" src="/plot/stddev" style="width: 100%; max-width: 600px;">
    </div>

    <div>
        <h2>Individual Chart</h2>
        <img id="individual_chart" src="/plot/individual" style="width: 100%; max-width: 600px;">
    </div>

    <div>
        <h2>Moving Range Chart</h2>
        <img id="moving_range_chart" src="/plot/moving_range" style="width: 100%; max-width: 600px;">
    </div>

    <a href="/plot">Back to Chart Selection</a>

    <script>
        const socket = io.connect('http://localhost:8080');

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

