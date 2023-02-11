from threading import Thread
from imutils.video import VideoStream
import imagezmq
import zmq
import adafruit_pca9685
import time
import sys
import os
import json


class CameraGimbal:

    def __init__(self, channel):
        self.channel = channel
    
    def set_angle(self, angle):
        pass
    

class MotorT200:

    # Someone still needs to test and work on this, I am not sure if I am using the correct syntax for esc control. This could be something for @AI-YT to do

    def __init__(self, channel, controller):
        self.channel = channel
        self.controller = controller

        self.stop = 1500
        self.full_forward = 1900
        self.full_reverse = 1100

        self.DIFF = self.full_forward - self.full_reverse

        self.pwm = self.stop
    
    def bootup_signal(self):
        boot = self.stop
        self.controller[self.channel].frequency = 100
        self.controller[self.channel].duty_cycle = boot
    
    def throttle(self, t):
        assert type(t) == float and t <= 1.0 and t >= -1.0
        diff = t/2*self.DIFF
        self.pwm = self.stop+diff
        self.controller[self.channel].duty_cycle = self.pwm
        

class MotorController(Thread):

    #AS OF RIGHT NOW, I AM UNSURE OF MOTOR CONFIGURATION FOR THE UD MOTORS

    #CURRENT MOTOR CONTROL CONFIGURATION (*=camera):
    """

        /         \ 
       \           /
        A_________B
        |   |*|   |
        |E  | |  F|
        |   | |   |
     \  C_________D /
       /           \ 
    
       Direction of thrust (the way the motor pushes the robot) is shown by the secondary arrows.
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

        for thruster in self.thrusters:
            thruster.bootup_signal()
        time.sleep(8)

        self.camera_gimbal = CameraGimbal(camera_gimbal)

        self.full_forward_grid_throttles = (-1.0, -1.0, 1.0, 1.0, 0.0, 0.0)
        self.full_right_grid_throttles = (-1.0, 1.0, 1.0, -1.0, 0.0, 0.0)
        self.full_left_grid_throttles = (1.0, -1.0, -1.0, 1.0, 0.0, 0.0)
        self.full_back_grid_throttles = (1.0, 1.0, -1.0, -1.0, 0.0, 0.0)

        self.full_down_throttles = (0.0, 0.0, 0.0, 0.0, 1.0, 1.0)
        self.full_up_throttles = (0.0, 0.0, 0.0, 0.0, -1.0, -1.0)

    def full_forward(self):
        a, b, c, d, e, f = self.full_forward_grid_throttles
        self.throttle_thrusters([a, b, c, d, e, f])
    
    def full_right(self):
        a, b, c, d, e, f = self.full_right_grid_throttles
        self.throttle_thrusters([a, b, c, d, e, f])
    
    def full_left(self):
        a, b, c, d, e, f = self.full_left_grid_throttles
        self.throttle_thrusters([a, b, c, d, e, f])
    
    def full_back(self):
        a, b, c, d, e, f = self.full_back_grid_throttles
        self.throttle_thrusters([a, b, c, d, e, f])
    
    def full_down(self):
        a, b, c, d, e, f = self.full_down_throttles
        self.throttle_thrusters([a, b, c, d, e, f])
    
    def full_up(self):
        a, b, c, d, e, f = self.full_up_throttles
        self.throttle_thrusters([a, b, c, d, e, f])

    def get_throttle_x(self, t):
        throttles = [elem*t for elem in [1.0, 1.0, 1.0, 1.0, 0.0, 0.0]]
        return throttles

    def get_throttle_y(self, t):
        throttles = [elem*t for elem in [1.0, -1.0, -1.0, 1.0, 0.0, 0.0]]
        return throttles
    
    def get_throttle_xy(self, xt, yt):
        x_throttle = self.get_throttle_x(xt)
        y_throttle = self.get_throttle_y(yt)
        xy_throttle = []

        for i in range(len(x_throttle)):
            s = x_throttle[i] + y_throttle[i]
            xy_throttle.append(s/2.0)
        
        return xy_throttle

    def get_throttle_xyz(self, xt, yt, te, tf):
        xy_throttles = self.get_throttle_xy(xt, yt)

        xy_throttles[5], xy_throttles[6] = te, tf

        return xy_throttles
    

    def set_camera_gimbal(self, angle):
        self.camera_gimbal.set_angle(angle)
    
    def throttle_thrusters(self, throttles):
        assert len(throttles) == 6

        for i, t in enumerate(throttles):
            self.thrusters[i].throttle(t)
        
    def xy_throttle(self, joy_x, joy_y):
        throttles = self.get_throttle_xy(joy_x, joy_y)
        self.throttle_thrusters(throttles)
    
    def run(self):
        on = True
        
        while on:
            message = json.loads(self.socket.recv())
            print(message)
            xax = message['x']
            yax = message['y']
            ezax = message['e']
            fzax = message['f']

            throttles = self.get_throttle_xyz(xax, yax, ezax, fzax)
            self.throttle_thrusters(throttles)
            
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