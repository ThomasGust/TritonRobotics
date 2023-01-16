import numpy as np
print(np.__version__)

import cv2
print(cv2.__version__)

cam = cv2.VideoCapture(0)

result, img = cam.read()

if result:
    cv2.imwrite("/home/tritonrobotics2/Desktop/TESTIMAGE1.jpg", img)
    print("saved image")

else:
    print("NO RESULT")