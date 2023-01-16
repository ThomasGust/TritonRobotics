import numpy as np
print(np.__version__)

import cv2
print(cv2.__version__)


cam = cv2.VideoCapture(0)

def capture(name):
    result, img = cam.read()

    if result:
        cv2.imwrite(f"/home/tritonrobotics2/Desktop/{name}.jpg", img)
        print("saved image")

    else:
        print("NO RESULT")

if __name__ == "__main__":
    capture("TESTIMAGE1")