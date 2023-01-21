import socket
import imagezmq
import cv2

sender = imagezmq.ImageSender(connect_to='tcp://169.254.222.33:5555')

sender_name = socket.gethostname() # send your hostname with each image

image = cv2.imread("test1.png")
print(type(image))
sender.send_image_pubsub(sender_name, image)