import cv2


cam = cv2.VideoCapture(0)

result, img = cam.read()

if result:
    cv2.imwrite("IMG.png", img)
    print("saved image")

else:
    print("NO RESULT")