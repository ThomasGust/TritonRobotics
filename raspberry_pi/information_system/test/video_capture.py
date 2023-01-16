import numpy as np
import time
import matplotlib.pyplot as plt
print(np.__version__)

import cv2
print(cv2.__version__)

#CV2.imwrite says it does not have permission
def imwrite(name, img):
    plt.imshow(img)
    plt.savefig(name)
cam = cv2.VideoCapture(0)

result, img = cam.read()

if result:
    imwrite("Desktop\\TESTIMAGE1.jpg", img)
    print("saved image")

else:
    print("NO RESULT")