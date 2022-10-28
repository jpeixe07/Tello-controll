from djitellopy import tello
import cv2

me = tello.Tello()
me.connect()
print(me.get_battery())

me.streamon()

while True:
    frame = me.get_frame_read().frame
    frame = cv2.resize(frame, (360, 240))
    cv2.imshow("Image", frame)
    cv2.waitKey(1)