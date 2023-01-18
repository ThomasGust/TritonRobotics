import socket
from threading import Thread
from utils import get_camera, encode_image, snap



class Topside(Thread):

    def __init__(self, bottomside, port=5005, buffer_size=724288):
        Thread.__init__(self)

        self.bottomside = bottomside
        self.port = port
        self.bs = buffer_size

        self.mc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mc_socket.connect((self.bottomside, self.port))

        self.camera = get_camera()
    def run(self):
        msg = encode_image(snap(self.camera))
        self.mc_socket.send(msg)
        



if __name__ == "__main__":
    ip_addr = '169.254.82.153'
    top = Topside(ip_addr)
    top.run()