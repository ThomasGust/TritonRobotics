import imagezmq
import cv2

image_hub = imagezmq.ImageHub()
print("INITIALIZED IAMGE HUB")
sender_name, image = image_hub.recv_image()
print("RECEIVED IMAGE")
image_hub.send_reply(b'OK')
print("RECEIVED IMAGE")

cv2.imshow("THIS IS A TEST", image)
cv2.waitKey(0)