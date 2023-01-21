import socket
import imagezmq
import cv2
from imutils.video import VideoStream

sender = imagezmq.ImageSender(connect_to='tcp://169.254.222.33:5555')

webcam = VideoStream().start()
sender_name = socket.gethostname() # send your hostname with each image

while True:
    image = webcam.read()
    print(type(image))
    sender.send_image_pubsub(sender_name, image)