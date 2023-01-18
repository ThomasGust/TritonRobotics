import cv2
import base64

cam = cv2.VideoCapture(0)

codec = 0x47504A4D  # MJPG
cam.set(cv2.CAP_PROP_FPS, 30.0)
cam.set(cv2.CAP_PROP_FOURCC, codec)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)


def capture(name):
    result, img = cam.read()

    if result:
        #cv2.imwrite(f"/home/tritonrobotics2/Desktop/{name}.jpg", img)
        retval, buffer = cv2.imencode('.jpg', img)
        pg_as_text = base64.b64encode(buffer)
        decoded = base64.b64decode(pg_as_text)

        with open(f'{name}.jpg', "wb") as f:
            f.write(decoded)
        print("saved image")

    else:
        print("NO RESULT")

if __name__ == "__main__":
    name = input("Please enter an image name here without an extension: ")
    capture(name)