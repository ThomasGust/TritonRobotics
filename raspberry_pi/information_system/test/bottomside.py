import socket
from threading import Thread


class BottomSide(Thread):

    def __init__(self, host, mc_port=5005, buffer_size=1024):
        Thread.__init__(self)
        self.host = host
        self.mc_port = mc_port
        self.buffer_size = buffer_size

        self.mc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mc_socket.bind((self.host, self.mc_port))
    
    def run(self):
        self.mc_socket.listen(1)
        connection, address = self.mc_socket.accept()

        print(address)

        on = True

        while on:
            data = self.mc_socket.recv(self.buffer_size)
            if not data: on = False
            print(data)
            connection.send(data)
        connection.close()
    
def start_server(IP):
    #IP = 'PUT SERVER IP (RASPI) HERE'
    PORT = 5005
    BS = 1024

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((IP, PORT))
    sock.listen(1)

    connection, address = sock.accept()

    print(f"ADDR: {address}")

    while 1:
        data = connection.recv(BS)
        if not data: break
        print(f"received: {data}")
        connection.send(data)
    connection.close()

if __name__ == "__main__":
    ip_addr = input("Please put server ip address here: ")
    bottom = BottomSide(ip_addr)
    bottom.run()