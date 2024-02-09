import eventlet
import eventlet.wsgi
eventlet.monkey_patch()
import datetime
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)

global current_image
current_image = ""

@socketio.on("connect")
def test_connect():
    print("Connected")
    emit("my response", {"data": "Connected"})

@socketio.on("test")
def test(data):
    global current_image
    #print(data[:10])
    current_image = data
    
@socketio.on("image")
def receive_image(image):
    global current_image
    print(f'time: {datetime.datetime.now()}/hash: {current_image[:10]}')
    emit("processed_image", "data:image/jpeg;base64,"+current_image)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    socketio.run(app, debug=True, port=8080)