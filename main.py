# gunicorn -b :8080 --worker-class eventlet -w 1 main:app
# kill -9 $(lsof -t -i:"8080")
import eventlet
import eventlet.wsgi
eventlet.monkey_patch()
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)
DRONE_IDS = ["UAV-1234"]

class AppData:
    client = ""
    vehicle = ""
    marker = {"lat": 0, "lon": 0, "alt": 0}
    id = ""

global appData
appData = AppData()

@socketio.on("update_sid")
def update_sid():
    global appData
    appData.client = request.sid
    print(f'client sid updated: {appData.client}')
    if appData.marker["lat"] != 0:
        emit("init_marker", {"id": appData.id, "lat": appData.marker["lat"], "lon": appData.marker["lon"], "alt": appData.marker["alt"]}, room=appData.client)

@socketio.on("connect")
def test_connect():
    emit("conn_success", {"data": "Connected"})

@socketio.on("disconnect")
def disconnect():
    global appData
    if request.sid == appData.vehicle:
        appData.id = ""

@socketio.on("ready")
def ready(data):
    global appData
    if appData.vehicle != "":
        emit("ready", data, room=appData.vehicle)

@socketio.on("vehicle_sign_in")
def vehicle_sign_in(data):
    if data["id"] in DRONE_IDS:
        global appData
        appData.vehicle = request.sid
        appData.id = data["id"]
        appData.marker["lat"] = data["lat"]
        appData.marker["lon"] = data["lon"]
        appData.marker["alt"] = data["alt"]
        print(f'vehicle sid updated: {appData.vehicle}')
        emit("init_marker", data, room=appData.client)

@socketio.on("stream")
def stream(data):
    global appData
    emit("update_vehicle", {"image": "data:image/jpeg;base64," + data["frame"], "params": data["log"]}, room=appData.client)
    
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    socketio.run(app, debug=True, port=8080)