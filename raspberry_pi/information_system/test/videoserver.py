import socketio
import base64


sio = socketio.Server()


@sio.on('data')
def handle_image(data_image):
    print('received image')