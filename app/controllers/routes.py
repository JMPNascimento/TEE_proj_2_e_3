from app.controllers.application import Application
from bottle import Bottle, request, response, template, TEMPLATE_PATH
from app.models.SPC import ControlChart
from app.models.graph import *
from io import BytesIO
import socketio
import base64
import os

app = Bottle()
sio = socketio.Server(cors_allowed_origins="*")
app.wrap_app = socketio.WSGIApp(sio, app)

ctl = Application()
app.config['template_path'] = ['./views']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATE_DIR = os.path.join(BASE_DIR, "views")
TEMPLATE_PATH.insert(0, TEMPLATE_DIR)


control_chart = ControlChart()
control_chart.generate_data()
control_chart.calculate_statistics()

#-----------------------------------------------------------------------------
# WebSocket Events

@sio.on('connect')
def handle_connect(sid, environ):
    print(f"Client {sid} connected")

@sio.on('update_data')
def update_data(sid, new_data):
    control_chart.update_data(new_data)
    control_chart.calculate_statistics()

    send_chart_updates()

def send_chart_updates():
    charts = {
        "mean": generate_chart(XChartRenderer(control_chart)),
        "amplitude": generate_chart(RChartRenderer(control_chart)),
        "stddev": generate_chart(sChartRenderer(control_chart)),
        "individual": generate_chart(IndividualChartRenderer(control_chart)),
        "moving_range": generate_chart(MovingRangeChartRenderer(control_chart)),
    }

    sio.emit('chart_update', charts)

def generate_chart(chart_renderer):
    img_buffer = BytesIO()
    chart_renderer.render().save(img_buffer, format="PNG") 
    img_buffer.seek(0)
    
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode("utf-8")
    
    return {"image": img_base64}

@app.route('/update_data', method='POST')
def update_data(new_data):
    print(f"Received raw new_data: {new_data}")  # Debugging
    
    # 🛠 Ensure new_data is a valid list of numbers
    if not isinstance(new_data, list):
        raise ValueError("Received data is not a list.")
    
    # Filter out non-numeric values
    cleaned_data = [x for x in new_data if isinstance(x, (int, float))]

    # Ensure it's a list of lists (SPC expects it)
    formatted_data = [cleaned_data] if isinstance(cleaned_data[0], (int, float)) else cleaned_data

    print(f"Formatted new_data: {formatted_data}")  # Debugging check

    # Pass to control chart
    control_chart.update_data(np.array(formatted_data, dtype=np.float64))


#-----------------------------------------------------------------------------
# Routes:

@app.route('/plot')
def plots_page():
    return template("plot.tpl", chart_url="/plot/mean")

# app.run(debug=True, reloader=True, template_lookup=["views"])

@app.route('/plot/mean')
def plot_mean():
    return generate_chart(XChartRenderer(control_chart))

@app.route('/plot/amplitude')
def plot_amplitude():
    return generate_chart(RChartRenderer(control_chart))

@app.route('/plot/stddev')
def plot_stddev():
    return generate_chart(sChartRenderer(control_chart))

@app.route('/plot/individual')
def plot_individual():
    return generate_chart(IndividualChartRenderer(control_chart))

@app.route('/plot/moving_range')
def plot_moving_range():
    return generate_chart(MovingRangeChartRenderer(control_chart))

#-----------------------------------------------------------------------------