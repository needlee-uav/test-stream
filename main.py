import eventlet
import eventlet.wsgi
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, CORS_ALLOW_ALL_ORIGINS=True)

@socketio.on("connect")
def test_connect():
    print("Connected")
    emit("my response", {"data": "Connected"})

@socketio.on("test")
def test(data):
    global current_image
    current_image = data
    
@socketio.on("image")
def receive_image():
    global current_image
    emit("processed_image", current_image)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    socketio.run(app, debug=True, port=8080)