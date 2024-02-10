import eventlet
import eventlet.wsgi
eventlet.monkey_patch()
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)

client = ""

@socketio.on("update_sid")
def update_sid():
    client = request.sid
    print(f'client sid updated: {client}')

@socketio.on("connect")
def test_connect():
    emit("conn_success", {"data": "Connected"})

@socketio.on("stream")
def stream(data):
    emit("processed_image", "data:image/jpeg;base64," + data, room=client)
    
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    socketio.run(app, debug=True, port=8080)