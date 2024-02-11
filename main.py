# KILL ON TESTS: kill -9 $(lsof -t -i:"8080")
import eventlet
import eventlet.wsgi
eventlet.monkey_patch()
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)

client = ""
marker = {"lat": 0, "lon": 0, "alt": 0}

@socketio.on("update_sid")
def update_sid():
    client = request.sid
    print(f'client sid updated: {client}')
    if marker["lat"] != 0:
        print(marker)
        emit("init_marker", {"lat": marker["lat"], "lon": marker["lon"], "alt": marker["alt"]}, room=client)

@socketio.on("connect")
def test_connect():
    emit("conn_success", {"data": "Connected"})

@socketio.on("move_map_to_vehicle")
def move_map_to_vehicle(data):
    print("recieved move map")
    marker["lat"] = data["lat"]
    marker["lon"] = data["lon"]
    marker["alt"] = data["alt"]
    emit("init_marker", data, room=client)
    
@socketio.on("stream")
def stream(data):
    emit("update_vehicle", {"image": "data:image/jpeg;base64," + data["frame"], "params": data["log"]}, room=client)
    
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    socketio.run(app, debug=True, port=8080)