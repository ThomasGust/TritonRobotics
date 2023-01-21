import socket
import imagezmq

sender = imagezmq.ImageSender(connect_to='tcp://169.254.82.153:5555')

sender_name = socket.gethostname() # send your hostname with each image

image = open("test1.jpg",'rb')
sender.send_image(sender_name, image)