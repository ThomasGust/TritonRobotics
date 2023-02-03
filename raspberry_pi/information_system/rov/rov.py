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
    
    def __init__(self, name):
        Thread.__init__(self)
        self.webcam = VideoStream().start()
        self.name = name
    

    def run(self, client_ip, client_vid_port):
        sender = imagezmq.ImageSender(connect_to=f"{client_ip}:{client_vid_port}")
        
        on = True

        while on:
            img = self.webcam.read()
            sender.send_image_reqrep(self.name, img)

class Rov:

    def __init__(self):
        self.image_sender = ImageSender(name="TritonROV")
    
    def control_loop(self):
        self.image_sender.start()
