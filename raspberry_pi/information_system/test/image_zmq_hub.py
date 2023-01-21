import cv2
import imagezmq
hub = imagezmq.ImageHub()
print("INITIALIZED HUB")
while True:
    name, frame = hub.recv_image()
    print("RECEIVED IMAGE")
    cv2.imshow(name, frame)
    cv2.waitKey(1)
    hub.send_reply(b'OK')