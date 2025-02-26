from app.controllers.routes import app
import eventlet
import eventlet.wsgi

if __name__ == '__main__':
    print("Starting server on http://localhost:8080")
    eventlet.wsgi.server(eventlet.listen(("0.0.0.0", 8080)), app.wrap_app)