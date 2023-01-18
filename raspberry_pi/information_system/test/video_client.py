import socket
from utils import decode_image
from threading import Thread
    

class BottomSide(Thread):

    def __init__(self, host, mc_port=5005, buffer_size=724288):
        Thread.__init__(self)
        self.host = host
        self.mc_port = mc_port
        self.buffer_size = buffer_size

        self.mc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mc_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.mc_socket.bind((self.host, self.mc_port))

        self.power = 10
    
    def run(self):
        self.mc_socket.listen(1)
        connection, address = self.mc_socket.accept()

        img = decode_image(self.mc_socket.recv(self.buffer_size))
        connection.close()


if __name__ == "__main__":
    ip_addr = '169.254.82.153'
    bottom = BottomSide(ip_addr)
    bottom.run()