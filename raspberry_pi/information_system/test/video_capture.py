import numpy as np
import time
import matplotlib.pyplot as plt
print(np.__version__)

import cv2
print(cv2.__version__)


cam = cv2.VideoCapture(0)

result, img = cam.read()

if result:
    plt.imshow(img)
    plt.show()
    time.sleep(10)
    print("saved image")

else:
    print("NO RESULT")