import cv2
from io import BytesIO
import base64
from imageio import imread
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True
def get_camera(h=1080//4, w=1920//4):
    cam = cv2.VideoCapture(0)

    codec = 0x47504A4D  # MJPG
    cam.set(cv2.CAP_PROP_FPS, 30.0)
    cam.set(cv2.CAP_PROP_FOURCC, codec)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
    return cam

def snap(cam):
    result, img = cam.read()
    if result: return img
    else: return None


def encode_image(img):
    retval, buffer = cv2.imencode('.jpg', img)
    return base64.b64encode(buffer)
    #decoded = base64.b64decode(pg_as_text)

def decode_image(b64_img):
    return imread(BytesIO(base64.b64decode(b64_img)))
