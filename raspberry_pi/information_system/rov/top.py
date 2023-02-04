import imagezmq
from threading import Thread
import cv2
import socket

class ImageReceiver(Thread):

    def __init__(self, top_ip, port=5555):
        self.hub = imagezmq.ImageHub(open_port=f'tcp://{top_ip}:{port}')
    
    def run(self):

        on = True

        while on:

            sender_name, image = self.hub.recv_image()
            self.hub.send_reply(b"RI")
            print(image.shape)


class Top:

    def __init__(self, video_receiver_port=5555):
        self.video_receiver_port = video_receiver_port
        self.image_receiver = ImageReceiver(socket.gethostbyname(), video_receiver_port)

    def control_loop(self):
        self.image_receiver.start()


if __name__ == "__main__":
    topside = Top()
    topside.control_loop()
        
