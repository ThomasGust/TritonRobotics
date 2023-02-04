from threading import Thread
from imutils.video import VideoStream
import imagezmq

class Motor:

    def __init__(self):
        pass

class MotorController:

    def __init__(self):
        pass


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

    def __init__(self, client_ip, client_vid_port, name):
        self.image_sender = ImageSender(client_ip, client_vid_port, name)
    
    def control_loop(self):
        self.image_sender.start()

if __name__ == "__main__":
    client_ip = ""
    client_vid_port = 5555
    rov = Rov(client_ip, client_vid_port, "MainROV")
    rov.control_loop()