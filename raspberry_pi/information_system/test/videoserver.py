from flask_socketio import emit, SocketIO
from flask import Flask

app = Flask(__name__)


sio = SocketIO(app)


@sio.on('data')
def handle_image(data_image):
    print('received image')

if __name__ == "__main__":
    h = input('Please input a valid ip address for the server: ')
    sio.run(app, host=h, port=5005)