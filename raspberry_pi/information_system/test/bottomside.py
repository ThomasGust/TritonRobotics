import socket
from threading import Thread
#import cv2
import base64
#import matplotlib.pyplot as plt
#import numpy as np
import time
import pigpio

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

class Controller():

    def __init__(self, p1=27, p2=22, forw=1900, stop=1500, reve=1100, init=1500):
        self.pi = pigpio.pi()

        self.p1, self.p2 = p1, p2

        self.FORW = forw
        self.STOP = stop
        self.REVE = reve
        self.INIT = init

        self.pwm1 = self.INIT
        self.pwm2 = self.INIT

        self.DIFF = self.FORW - self.REVE

        
        self.setup(self.p1, self.p2)

    def get_pins(self, p1=27, p2=22):
        self.pi.set_mode(p1, pigpio.OUTPUT)
        self.pi.set_mode(p2, pigpio.OUTPUT)
        print("FINISHED SETTING UP PINS")

    def initialize_escs(self, e1, e2):
        self.pi.set_servo_pulsewidth(e1, self.INIT)
        time.sleep(8)
        self.pi.set_servo_pulsewidth(e2, self.INIT)
        time.sleep(8)
        print("INITIALIZED ESCS")

    
    def setup(self, p1, p2):
        self.get_pins(p1, p2)
        self.initialize_escs(p1, p2)
    
    def throttle_servos(self, power1, power2):
        assert power1 >= -1.00 and power1 <= 1.00 and power2 >= -1.00 and power2 <= 1.00

        diff1 = int(power1/2*self.DIFF)
        diff2 = int(power2/2*self.DIFF)

        self.pwm1 = self.STOP+diff1
        self.pwm2 = self.STOP+diff2

        self.pi.set_servo_pulsewidth(self.p1, self.pwm1)
        self.pi.set_servo_pulsewidth(self.p2, self.pwm2)
    

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

        print(address)

        on = True

        controller = Controller()
        while on:
            data = connection.recv(self.buffer_size).decode()
            if not data: on = False

            if data == "W":
                controller.throttle_servos(self.power/10, self.power/10)

            if data == "A":
                controller.throttle_servos(-self.power/10, self.power/10)

            if data == "S":
                controller.throttle_servos(-self.power/10, -self.power/10)
                
            if data == "D":
                controller.throttle_servos(self.power/10, -self.power/10)
                
            if data == "P":
                controller.throttle_servos(0.0, 0.0)
                
            if data == "KU":
                if self.power+1 <= 10.1:
                    self.power += 1
                
            if data == "KD":
                if self.power-1 >= -0.1:
                    self.power -=1
            
            print(self.power, controller.pwm1, controller.pwm2)

        connection.close()
    """
    def encode_image(self, img):
        encoded = cv2.imencode('.jpg', img)[1]
        stringData = base64.b64encode(encoded).decode('utf-8')
        b64_src = 'data:image/jpeg;base64,'

        stringData = b64_src + stringData
        print(len(stringData))
        return stringData
    
    def take_picture(self):
        result, img = self.cam.read()
        #img = cv2.resize(img, (, 1))

        if result:
            return img
        else:
            return None

    """
    
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