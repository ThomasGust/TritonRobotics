import socketio
import base64
from flask_socketio import emit, SocketIO
from flask import Flask

app = Flask(__name__)


sio = SocketIO(app)


@sio.on('data')
def handle_image(data_image):
    print('received image')

if __name__ == "__main__":
    app.run()