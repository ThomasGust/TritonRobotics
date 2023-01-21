import imagezmq
import cv2

image_hub = imagezmq.ImageHub()

sender_name, image = image_hub.recv_image()
image_hub.send_reply(b'OK')
print("RECEIVED IMAGE")

cv2.imshow("THIS IS A TEST", image)
cv2.waitKey(0)