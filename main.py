import base64
import os
import eventlet
import eventlet.wsgi
eventlet.monkey_patch()

import cv2
import numpy as np
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_folder="./static")
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, CORS_ALLOW_ALL_ORIGINS=True)
global current_image 
current_image = None


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


def base64_to_image(base64_string):
    # Extract the base64 encoded binary data from the input string
    base64_data = base64_string.split(",")[1]
    # Decode the base64 data to bytes
    image_bytes = base64.b64decode(base64_data)
    # Convert the bytes to numpy array
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    # Decode the numpy array as an image using OpenCV
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image


@socketio.on("connect")
def test_connect():
    print("Connected")
    emit("my response", {"data": "Connected"})

@socketio.on("test")
def test(data):
    global current_image
    # image = base64_to_image("data:image/jpeg;base64,"+data)
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # frame_resized = cv2.resize(gray, (640, 360))

    # encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    # result, frame_encoded = cv2.imencode(".jpg", frame_resized, encode_param)

    # processed_img_data = base64.b64encode(frame_encoded).decode()

    b64_src = "data:image/jpg;base64,"
    processed_img_data = b64_src + data
    current_image = processed_img_data
    


@socketio.on("image")
def receive_image(image):
    global current_image
    # Decode the base64-encoded image data
    #print(image)
    # image = base64_to_image(image)

    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # frame_resized = cv2.resize(gray, (640, 360))

    # encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    # result, frame_encoded = cv2.imencode(".jpg", frame_resized, encode_param)

    # processed_img_data = base64.b64encode(frame_encoded).decode()

    # b64_src = "data:image/jpg;base64,"
    # processed_img_data = b64_src + processed_img_data
    print(str(current_image)[:10])
    emit("processed_image", current_image)

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    socketio.run(app, debug=True, port=8080)
