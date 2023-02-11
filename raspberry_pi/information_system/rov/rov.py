from threading import Thread
from imutils.video import VideoStream
import imagezmq
import zmq
import adafruit_pca9685
import time
import sys
import os


class CameraGimbal:

    def __init__(self, channel):
        self.channel = channel
    
    def set_angle(self, angle):
        pass
    

class MotorT200:

    def __init__(self, channel):
        self.channel = channel
    
    def throttle(self, t):
        pass
        

class MotorController(Thread):

    #AS OF RIGHT NOW, I AM UNSURE OF MOTOR CONFIGURATION FOR THE UD MOTORS

    #CURRENT MOTOR CONTROL CONFIGURATION (*=camera):
    """
       \           /
        A_________B
        |   |*|   |
        |E  | |  F|
        |   | |   |
        C_________D
       /           \ 
    """

    def __init__(self, server_ip, server_port, motor_channels=[0, 1, 2, 3, 4, 5], camera_gimbal=6, context=zmq.Context()):
        
        Thread.__init__(self)

        self.zmq_context = context
        self.socket = self.zmq_context.socket(zmq.REP)
        self.socket.connect(f"tcp://{server_ip}:{server_port}")

        self.controller = adafruit_pca9685.PCA9685()

        assert len(motor_channels) == 6

        self.motor_a = MotorT200(motor_channels[0])
        self.motor_b = MotorT200(motor_channels[1])
        
        self.motor_c = MotorT200(motor_channels[2])
        self.motor_d = MotorT200(motor_channels[3])

        self.motor_e = MotorT200(motor_channels[4])
        self.motor_f = MotorT200(motor_channels[5])

        self.front = [self.motor_a, self.motor_b]
        self.mid = [self.motor_e, self.motor_f]
        self.back = [self.motor_c, self.motor_d]

        self.grid = [self.motor_a, self.motor_b, self.motor_c, self.motor_d]
        self.thrusters = [self.motor_a, self.motor_b, self.motor_c, self.motor_d, self.motor_e, self.motor_f]

        self.camera_gimbal = CameraGimbal(camera_gimbal)

    def set_camera_gimbal(self, angle):
        self.camera_gimbal.set_angle(angle)
    
    def throttle_thrusters(self, throttles):
        assert len(throttles) == 6

        for i, t in enumerate(throttles):
            self.thrusters[i].throttle(t)
    
    def run(self):
        on = True
        
        while on:
            message = self.socket.recv()
            print(message)
            self.socket.send(b"World!")

        


class ImageSender(Thread):
    
    def __init__(self, client_ip, client_vid_port, name):
        Thread.__init__(self)
        self.webcam = VideoStream().start()
        self.name = name
        self.client_ip = client_ip
        self.client_vid_port = client_vid_port
    

    def run(self):
        sender = imagezmq.ImageSender(connect_to=f"{self.client_ip}:{self.client_vid_port}")
        
        on = True

        while on:
            img = self.webcam.read()
            sender.send_image_reqrep(self.name, img)

class Rov:

    def __init__(self, client_ip, client_vid_port, client_control_port, name):
        self.image_sender = ImageSender(client_ip, client_vid_port, name)
        self.motor_controller = MotorController(client_ip, client_control_port)
    
    def control_loop(self):
        self.image_sender.start()
        self.motor_controller.start()

if __name__ == "__main__":
    client_ip = ""
    client_vid_port = 5555
    rov = Rov(client_ip, client_vid_port, "MainROV")
    rov.control_loop()