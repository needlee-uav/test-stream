from flask import Flask, render_template, request
import eventlet
import socketio
import eventlet.wsgi
import cv2
import numpy
import base64
sio = socketio.Server()#async_mode=async_mode)
app = Flask(__name__)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

dict1={}
i=0
@app.route('/')
def index():
	return render_template('index.html')

@sio.event()
def pingpong(sid):
	print("//////////////////////////")
	sio.emit("send_data", room=sid)

@sio.event
def connect(sid, data):	
	print("[INFO] Connect to the server")
	pingpong(sid)

@sio.event
def send(sid, data):
	global i
	if sid not in dict1:
		i+=1
		dict1[sid]=i
	key=dict1[sid]
	#convert(data)
	print("Reached here")
	sio.emit('response',{'key':key, 'data':'nice'})
	sio.emit('image', data)
	pingpong(sid)

def convert(data):
	# cv2.imshow('g', data)
	# cv2.waitKey()
	#img = cv2.imread('test.jpg')
	#_, im_arr = cv2.imencode('.jpg', img)  # im_arr: image in Numpy one-dim array format.
	#im_bytes = im_arr.tobytes()
	im_b64 = base64.b64encode(data)

@sio.event
def disconnect(sid):
	print("[INFO] disconnected from the server")

if __name__ == '__main__':
	eventlet.wsgi.server(eventlet.listen(('0.0.0.0',5000)), app)