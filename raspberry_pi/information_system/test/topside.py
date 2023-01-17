import socket
from threading import Thread
import pygame
import sys
import cv2
import base64
import numpy as np
from io import StringIO, BytesIO
from PIL import Image



class Topside(Thread):

    def __init__(self, bottomside, port=5005, buffer_size=724288):
        Thread.__init__(self)

        self.bottomside = bottomside
        self.port = port
        self.bs = buffer_size

        self.mc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mc_socket.connect((self.bottomside, self.port))

        pygame.init()
        pygame.display.set_caption("Triton Robotics ROV Controller")
        self.font = pygame.font.Font('freesansbold.ttf', 32)
    
    def run(self):
        msg = b'THIS IS A SIMPLE TEST MESSAGE'

        self.mc_socket.send(msg)
        
        power = 1.0

        screen = pygame.display.set_mode((300, 300))
        clock = pygame.time.Clock()
        while True:
            data = self.mc_socket.recv(self.bs)
            data = str(data)
            print(data)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    power = 0.0
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_w:
                        self.mc_socket.send(b"W")
                    
                    if event.key == pygame.K_s:
                        self.mc_socket.send(b"S")
                    
                    if event.key == pygame.K_a:
                        self.mc_socket.send(b"A")
                    
                    if event.key == pygame.K_p:
                        self.mc_socket.send(b"P")
                    
                    if event.key == pygame.K_d:
                        self.mc_socket.send(b"D")
                    
                    elif event.key == pygame.K_k:
                        self.mc_socket.send(b"K")
                        self.power = 0.0
                        self.mc_socket.close()
                        pygame.quit()
                        sys.exit()
                    
                    elif event.key == pygame.K_UP:
                        if power+0.1 < 1.0:
                            self.mc_socket.send(b"KU")
                            power += 0.1
                    
                    elif event.key == pygame.K_DOWN:
                        if power-0.1 > 0.0:
                            self.mc_socket.send(b"KD")
                            power -= 0.1
                
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_s or event.key == pygame.K_d:
                        self.mc_socket.send(b"P")
            
            screen.fill((255, 255, 255))
            text = self.font.render(f"Power: {power}", True, (0, 0, 0), (255, 255, 255))
            rect = text.get_rect()
            rect.topleft = (0, 0)

            screen.blit(text, rect)
            pygame.display.update()

            clock.tick(60)

if __name__ == "__main__":
    ip_addr = '169.254.222.33'
    top = Topside(ip_addr)
    top.run()