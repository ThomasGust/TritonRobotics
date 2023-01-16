import socket
from threading import Thread
import pygame
import sys

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
                        #self.throttle_servos(power, power)
                        self.mc_socket.send(b"W")
                    
                    if event.key == pygame.K_s:
                        #self.throttle_servos(-power, -power
                        self.mc_socket.send(b"S")
                    
                    if event.key == pygame.K_a:
                        self.mc_socket.send(b"A")
                    
                    if event.key == pygame.K_d:
                        self.mc_socket.send(b"D")
                    
                    if event.key == pygame.K_k:
                        self.mc_socket.send(b"K")
                        self.power = 0.0
                        self.mc_socket.close()
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

if __name__ == "__main__":
    ip_addr = input("Please provide an IP address for the server: ")
    top = Topside(ip_addr)
    top.run()