import socket
from threading import Thread
import cv2
import base64
import matplotlib.pyplot as plt

class MockController():

    def __init__(self, p1=27, p2=22, forw=1900, stop=1500, reve=1100, init=1500):

        self.FORW = forw
        self.STOP = stop
        self.REVE = reve
        self.INIT = init

        self.DIFF = self.FORW - self.REVE

        self.pwm1 = 1500
        self.pwm2 = 1500
    
    def throttle_servos(self, power1, power2):
        assert power1 >= -1.00 and power1 <= 1.00 and power2 >= -1.00 and power2 <= 1.00

        diff1 = int(power1/2*self.DIFF)
        diff2 = int(power2/2*self.DIFF)

        self.pwm1 = self.STOP+diff1
        self.pwm2 = self.STOP+diff2

class BottomSide(Thread):

    def __init__(self, host, mc_port=5005, buffer_size=1024):
        Thread.__init__(self)
        self.host = host
        self.mc_port = mc_port
        self.buffer_size = buffer_size

        self.mc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mc_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.mc_socket.bind((self.host, self.mc_port))
        
        self.cam = cv2.VideoCapture(0)
    
    def run(self):
        self.mc_socket.listen(1)
        connection, address = self.mc_socket.accept()

        print(address)

        on = True

        power = 1.0
        controller = MockController()
        while on:
            data = connection.recv(self.buffer_size).decode()
            if not data: on = False

            if data == "W":
                controller.throttle_servos(power, power)

            if data == "A":
                controller.throttle_servos(-power, power)

            if data == "S":
                controller.throttle_servos(-power, -power)
                
            if data == "D":
                controller.throttle_servos(power, -power)
                
            if data == "P":
                controller.throttle_servos(0.0, 0.0)
                
            if data == "KU":
                if power+0.1 <= 1.0:
                    power += 1
                
            if data == "KD":
                if power-0.1 <= 0.0:
                    power -=0.1
            
            picture = self.take_picture()
            plt.imshow(picture)
            plt.show()
            encoded = self.encode_image(picture)
            connection.send(bytes(encoded, encoding='utf-8'))
            print('took image')
            print()
            print(controller.pwm1, controller.pwm2, power)
            print()

        connection.close()
    
    def encode_image(self, img):
        encoded = cv2.imencode('.jpg', img)[1]
        stringData = base64.b64encode(encoded).decode('utf-8')
        b64_src = 'data:image/jpeg;base64,'

        stringData = b64_src + stringData
        return stringData
    
    def take_picture(self):
        result, img = self.cam.read()
        #img = cv2.resize(img, (, 1))

        if result:
            return img
        else:
            return None
    
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
    ip_addr = '169.254.222.33'
    bottom = BottomSide(ip_addr)
    bottom.run()