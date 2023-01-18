import socket
from threading import Thread
from utils import get_camera, encode_image, snap



class Topside(Thread):

    def __init__(self, bottomside, port=5005, buffer_size=724288):
        Thread.__init__(self)

        self.bottomside = bottomside
        self.port = port
        self.bs = buffer_size

        print("SOCKET INIT")
        self.mc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mc_socket.connect((self.bottomside, self.port))
        print("SOCKET CONNECT COMPLETED")

        self.camera = get_camera()
        print("INITIALIAZED CAMERA")
    def run(self):
        #msg = encode_image(snap(self.camera))
        msg = b'TESTING'
        print("Beginning to send image over ethernet")
        self.mc_socket.send(msg)
        print("FINISHED SENDING IMAGE")
        



if __name__ == "__main__":
    ip_addr = '169.254.222.33'
    top = Topside(ip_addr)
    top.run()