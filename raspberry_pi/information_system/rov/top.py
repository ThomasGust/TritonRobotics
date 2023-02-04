import imagezmq
from threading import Thread
import cv2
import socket
import zmq


class MotorControllerSender(Thread):
    

    def __init__(self, rov_ip, port, context):
        Thread().__init__(self)

        self.socket = context.socket(zmq.REP)
        self.socket.bind(f"tcp://{rov_ip}:{port}")
    
    def run(self):
        #RUN IS IN A TEST MODE FOR ZEROMQ MESSAGE PASSING
        on = True

        index = 0
        while on:
            print(f"Sending Request {index} ...")
            self.socket.send(b"Hello!")

            message =self. socket.recv()
            print(f"Received Reply {index} [ {message} ]")

            index += 1



class ImageReceiver(Thread):

    def __init__(self, top_ip, port=5555):
        Thread.__init__(self)
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

        self.hostname = socket.gethostbyname(socket.gethostname())

        self.zmq_context = zmq.Context()


        self.image_receiver = ImageReceiver(self.hostname, video_receiver_port)

    def control_loop(self):
        self.image_receiver.start()


if __name__ == "__main__":
    topside = Top()
    topside.control_loop()
