import socket
import imagezmq
import time
import cv2
from imutils.video import VideoStream

sender = imagezmq.ImageSender(connect_to='tcp://169.254.82.153:5555')

webcam = VideoStream().start()
sender_name = socket.gethostname() # send your hostname with each image
img = cv2.imread("test1.png")

while True:
    img = webcam.read()
    print("TOOK IMAGE")
    sender.send_image_reqrep(sender_name, img)