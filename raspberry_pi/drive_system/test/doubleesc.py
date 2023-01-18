import time
import pigpio
import pygame
import sys


class Controller():

    def __init__(self, p1=13, p2=12, forw=1900, stop=1500, reve=1100, init=1500):
        self.pi = pigpio.pi()

        self.p1, self.p2 = p1, p2

        self.FORW = forw
        self.STOP = stop
        self.REVE = reve
        self.INIT = init

        self.DIFF = self.FORW - self.REVE

        
        self.setup(self.p1, self.p2)

    def get_pins(self, p1=13, p2=12):
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

    
    def forward_full(self, t):
        self.pi.set_servo_pulsewidth(self.p1, self.FORW)
        self.pi.set_servo_pulsewidth(self.p2, self.FORW)
        time.sleep(t)

    def reverse_full(self, t):
        self.pi.set_servo_pulsewidth(self.p1, self.REVE)
        self.pi.set_servo_pulsewidth(self.p2, self.REVE)
        time.sleep(t)
    
    def turn_one_full(self, t):
        self.pi.set_servo_pulsewidth(self.p1, self.REVE)
        self.pi.set_servo_pulsewidth(self.p2, self.FORW)
        time.sleep(t)

    def turn_two_full(self, t):
        self.pi.set_servo_pulsewidth(self.p1, self.FORW)
        self.pi.set_servo_pulsewidth(self.p2, self.REVE)
        time.sleep(t)
    
    def stop(self):
        self.pi.set_servo_pulsewidth(self.p1, self.STOP)
        self.pi.set_servo_pulsewidth(self.p2, self.STOP)
    
    def throttle_servos(self, power1, power2):
        assert power1 >= -1.00 and power1 <= 1.00 and power2 >= -1.00 and power2 <= 1.00

        diff1 = int(power1/2*self.DIFF)
        diff2 = int(power2/2*self.DIFF)

        pow1 = self.STOP+diff1
        pow2 = self.STOP+diff2

        self.pi.set_servo_pulsewidth(self.p1, pow1)
        self.pi.set_servo_pulsewidth(self.p2, pow2)

    def wasd(self):
        power = 1.0
        pygame.init()

        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    power = 0.0
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_w:
                        self.throttle_servos(power, power)
                    
                    if event.key == pygame.K_s:
                        self.throttle_servos(-power, -power)
                    
                    if event.key == pygame.K_a:
                        self.throttle_servos(-power, power)
                    
                    if event.key == pygame.K_d:
                        self.throttle_servos(power, -power)
                    
                    if event.key == pygame.K_k:
                        self.power = 0.0
                        pygame.quit()
                        sys.exit()
                    
                    if event.key == pygame.K_UP:
                        if power+0.002 < 1.0:
                            power += 0.002
                            print(power)
                    
                    if event.key == pygame.K_DOWN:
                        if power-0.002 > 0.0:
                            power -= 0.002
                            print(power)
            
            clock.tick(60)
        
    def test(self):
        print("BEGINNING TEST")
        self.forward_full(4)
        print("END OF TEST")

if __name__ == "__main__":
    controller = Controller()
    controller.test()