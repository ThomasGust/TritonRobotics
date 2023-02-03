from adafruit_servokit import ServoKit
import time


class MotorController:

    def __init__(self, escs=[0, 1, 2, 3, 4, 5], gimbal=7):
        self.escs = escs
        self.gimbal = gimbal

        self.controller = ServoKit(channels=16)

        #COULD BE SERVO NOT CONTINOUS SERVO #TODO
 
        for e in escs:
            self.controller.servo[e].set_pulse_width_range(1100, 1900)
        
        self.setup()

    def setup(self):
        for e in self.escs:
            self.controller[e].throttle =  0
        time.sleep(8)

    def throttle_escs(self, throttles=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0]):
        for i, e in enumerate(self.escs):
            self.controller[e].throttle = throttles[i]
    