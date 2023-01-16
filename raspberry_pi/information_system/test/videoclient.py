import cv2
import socketio #python-socketio by @miguelgrinberg
import base64

sio = socketio.Client()

ip = input('Please provide a valid ip for video server: ')
sio.connect(f'{ip}:5005')

cam = cv2.VideoCapture(0)

while (True):
  ret, frame = cam.read()                     # get frame from webcam
  res, frame = cv2.imencode('.jpg', frame)    # from image to binary buffer
  data = base64.b64encode(frame)              # convert to base64 format
  sio.emit('data', data)                      # send to server