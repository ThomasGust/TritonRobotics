import socket
from utils import decode_image
from threading import Thread
import matplotlib.pyplot as plt
import time

class BottomSide(Thread):

    def __init__(self, host, mc_port=5005, buffer_size=100_000_0):
        Thread.__init__(self)
        self.host = host
        self.mc_port = mc_port
        self.buffer_size = buffer_size

        self.mc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("CREATED SOCKET")
        self.mc_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.mc_socket.bind((self.host, self.mc_port))
        print("BOUND SOCKET")

        self.power = 10
    
    def run(self):
        print("started listening")
        self.mc_socket.listen(1)
        connection, address = self.mc_socket.accept()
        print("CONNECTED")
        time.sleep(10)
        img = connection.recv(self.buffer_size)
        print(img)
        print(len(img))
        #plt.imshow(img)
        #plt.show()
        img = decode_image(img)
        plt.imshow(img)
        plt.show()
        print("RECEIVED IMAGE")
        connection.close()


if __name__ == "__main__":
    ip_addr = '169.254.222.33'
    bottom = BottomSide(ip_addr)
    bottom.run()