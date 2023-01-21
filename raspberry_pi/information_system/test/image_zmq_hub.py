import cv2
import imagezmq

image_hub = imagezmq.ImageHub()
print("INITIALIZED IMAGE HUB")

while True:
    sender_name, image = image_hub.recv_image()
    

    cv2.imshow("THIS IS A TEST", image)
    cv2.waitKey(1)

    image_hub.send_reply(b'OK')