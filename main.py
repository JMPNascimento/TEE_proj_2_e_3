from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from app.controllers.routes import app

if __name__ == '__main__':

    print("Starting server on http://localhost:8080")
    server = WSGIServer(("0.0.0.0", 8080), app.wrap_app, handler_class=WebSocketHandler)
    server.serve_forever()