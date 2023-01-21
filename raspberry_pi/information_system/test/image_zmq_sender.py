import socket
import time
from imutils.video import VideoStream
import imagezmq

sender = imagezmq.ImageSender(connect_to="tcp://169.254.82.153:5005")

name = socket.gethostname()

picam = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
while True:
    img = picam.read()
    sender.send_image_reqrep(name, img)