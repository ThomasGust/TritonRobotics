import imagezmq
from threading import Thread
import cv2
import socket
import zmq
import json
import pygame
from pygame.locals import *
import math
    

class MotorControllerSender(Thread):
    

    def __init__(self, rov_ip, port, context):
        Thread().__init__(self)

        pygame.init()
        self.socket = context.socket(zmq.REP)
        self.socket.bind(f"tcp://{rov_ip}:{port}")
        pygame.joystick.init()

        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

        self.xt = 0.0
        self.yt = 0.0
        self.et = 0.0
        self.ft = 0.0

    def format_message(self, x, y, e, f):
        message = {"x":x,
                   "y":y,
                   "e":e,
                   "f":f}
        message = json.dumps(message)
        return message


    def run(self):
        #ADD DEADZONE FOR JOYSTICK INPUT
        on = True

        index = 0
        while on:

            for event in pygame.event.get():
                if event.type == JOYBUTTONDOWN:
                    print(event)

                    if event.button == 0:
                        print("0")

                if event.type == JOYBUTTONDOWN:
                    print(event)
                
                if event.type == JOYAXISMOTION:
                    print(event)
                    "XBOX 360: (3, 4):right stick, (0, 1): left st;ick, left_trigger:2, right_trigger:5"

                    if event.axis == 0:
                        pass

                    if event.axis == 1:
                        self.et = event.value
                        self.ft = event.value

                    if event.axis == 3:
                        self.xt = event.value
                    
                    if event.axis == 4:
                        self.yt = event.value



                if event.type == JOYHATMOTION:
                    print(event)

            print(f"Sending Request {index} ...")
            self.socket.send(b"Hello")

            message =self. socket.recv()
            print(f"Received Reply {index} [ {message} ]")

            index += 1



class ImageReceiver(Thread):

    def __init__(self, top_ip, port=5555):
        Thread.__init__(self)
        self.hub = imagezmq.ImageHub(open_port=f'tcp://{top_ip}:{port}')
    
    def run(self):
        on = True

        while on:
            sender_name, image = self.hub.recv_image()
            self.hub.send_reply(b"RI")
            print(image.shape)



class Top:

    def __init__(self, motor_controller_port, video_receiver_port=5555):
        self.video_receiver_port = video_receiver_port

        self.hostname = socket.gethostbyname(socket.gethostname())

        self.zmq_context = zmq.Context()

        self.image_receiver = ImageReceiver(self.hostname, video_receiver_port)
        self.motor_controller = MotorControllerSender(self.hostname, motor_controller_port, self.zmq_context)

    def control_loop(self):
        self.image_receiver.start()
        self.motor_controller.start()


def joy_to_diff_drive(joy_x, joy_y):
    left = joy_x * math.sqrt(2.0)/2.0 + joy_y * math.sqrt(2.0)/2.0
    right = -joy_x * math.sqrt(2.0)/2.0 + joy_y * math.sqrt(2.0)/2.0
    return [left, right]

if __name__ == "__main__":
    #topside = Top()
    #topside.control_loop()
    print(joy_to_diff_drive(0.1, 0.1))
