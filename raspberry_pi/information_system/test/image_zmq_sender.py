import socket
import time
from imutils.video import VideoStream
import imagezmq

sender = imagezmq.ImageSender(connect_to="tcp://169.254.222.33:5005")

name = socket.gethostname()

picam = VideoStream().start()
time.sleep(2.0)
while True:
    img = picam.read()
    print("SENT IMAGE")
    sender.send_image_reqrep(name, img)