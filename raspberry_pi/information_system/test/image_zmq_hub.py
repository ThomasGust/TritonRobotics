import imagezmq

image_hub = imagezmq.ImageHub()

sender_name, image = image_hub.recv_image()
image_hub.send_reply(b'OK')