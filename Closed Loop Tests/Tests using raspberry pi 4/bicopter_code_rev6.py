#sudo killall pigpiod
import cv2
import os     #importing os library so as to communicate with the system
import time   #importing time library to make Rpi wait because its too impatient
sudoPassword='madypi'
command='killall pigpiod'
p=os.system('echo %s|sudo -S %s' % (sudoPassword, command))
os.system ("sudo pigpiod") #Launching GPIO library
#os.popen ("sudo -S %s"(sudo killall pigpiod),'w').write('madypi') #Launching GPIO library
time.sleep(1) # As i said it is too impatient and so if this delay is removed you will get an error
import pigpio #importing GPIO library

import numpy as np
import math


ESCR=19
#Connect the ESC in this GPIO pin
ESCL=13  #Connect the ESC in this GPIO pin

piR = pigpio.pi();
piL = pigpio.pi();
piR.set_servo_pulsewidth(ESCR, 1000)
piL.set_servo_pulsewidth(ESCL, 1000)
time.sleep(1)
cap = cv2.VideoCapture(0) # You may need to change the camera index depending on your system
startTime=0
throttle=1085
timee=time.time()
angle=0
integralVal=0
e=0
loopDuration=0
prevDuration=0
u=0
prev_e=0

kp=1 #3.3
ki=2
kd=0.3 #1.7

while True:
    ret, frame = cap.read()
     # Adaptive Thresholding
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)q
#     mean = np.mean(gray)
#     if mean < 100:
#         frame = cv2.convertScaleAbs(frame, alpha=70, beta=0)
#     elif mean > 200:
#         frame = cv2.convertScaleAbs(frame, alpha=0.5, beta=0)
    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # at a distance of 76 cm
    # Define the range of green color in HSV
    # Define the range of green color in HSV
    lower_green = np.array([90, 50, 50]) # 93
    upper_green = np.array([100, 255, 255]) # 94
    
    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_green, upper_green)
    kernel = np.ones((9, 9), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    # Find contours in the binary image
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw circles around the detected contours and calculate their centers
    centers = []
    for cnt in contours:
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        diameter = radius * 2
        center = (int(x), int(y))
        if diameter >= 50: # Only consider circles with a diameter greater than or equal to 100 pixels
            cv2.circle(frame, center, int(radius), (0, 255, 0), 2)
            centers.append(center)
    
    # Calculate the angle between any two detected centers
    if len(centers) == 2:
        for i in range(len(centers)-1):
            for j in range(i+1, len(centers)):
                center1 = centers[i]
                center2 = centers[j]
                dx = center2[0] - center1[0]
                dy = center2[1] - center1[1]
                angle = math.atan(dy/dx) * 180 / np.pi
                angle = round(angle,1)
                #cv2.putText(frame, f"Angle: {angle:.2f} deg", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
#                 if time.time()-startTime>=0.1:
#                     startTime=time.time()
#                     ser.write(str(angle).encode())  # encode the integer as a string and send it through serial


    
    # Display the resulting frame
    cv2.imshow('frame', kernel)
    prevDuration = timee
    timee = time.time()
    loopDuration = (timee - prevDuration)

    e = angle -0.7

    if (-0.5 < e < 0.5):
        integralVal = integralVal + (ki * e)

    u = (kp * e) + integralVal + (kd * ((e - prev_e) / loopDuration))
    
    if (u < -1000):
        u = -1000

    if (u > 1000):
        u = 1000

    round(throttle,0)
    leftSignal = throttle + u+45
    rightSignal = throttle - u-15

    #Right
    if (rightSignal < 1080):
        rightSignal = 1080
    
    if (rightSignal > 2000):
        rightSignal = 2000
    
    #Left
    if (leftSignal < 1100):
        leftSignal = 1080
    
    if (leftSignal >= 2000):
        leftSignal = 2000
    
    piR.set_servo_pulsewidth(ESCR, rightSignal)
    piL.set_servo_pulsewidth(ESCL, leftSignal)
    
    prev_e = e
    
    if cv2.waitKey(1) == ord('q'):
        piR.set_servo_pulsewidth(ESCR, 1000)
        piL.set_servo_pulsewidth(ESCL, 1000)
        break

cap.release()
cv2.destroyAllWindows()

