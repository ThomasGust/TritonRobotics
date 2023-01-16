import socket
from threading import Thread

class Topside(Thread):

    def __init__(self, bottomside, port=5005, buffer_size=1024):
        Thread.__init__(self)

        self.bottomside = bottomside
        self.port = port
        self.bs = buffer_size

        self.mc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mc_socket.connect((self.bottomside, self.port))
    
    def run(self):
        msg = b'THIS IS A SIMPLE TEST MESSAGE'

        self.mc_socket.send(msg)
        data = self.mc_socket.recv(self.bs)
        self.mc_socket.close()

def start_client(IP):
    #IP = 'PUT IP ADDRESS OF PC HERE'
    PORT = 5005
    BS = 1024

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP, PORT))
    sock.send(b"CLIENT: THIS IS A SIMPLE TEST TO SEE IF I CAN SEND DATA BETWEEN RASPBERRY PI AND COMPUTER OVER ETHERNET")
    data = sock.recv(BS)
    sock.close()

    print(f"received: {data}")

if __name__ == "__main__":
    ip_addr = input("Please provide an IP address for the server: ")
    top = Topside(ip_addr)
    top.run()