# Bicopter-Balancing
## A bicopter that uses a camera sensor and a computer vision algorithm in Python on an embedded Raspberry Pi 4 to balance a beam horizontally by actuating 2 BLDC Motors

#### The hardware consists of 2 BLDC Motors and a horizontal beam attached to their respective Electroic speed controllers(ESCs). After callibration, the 2 ESCs are connected to the raspberry pi 4, where the webcam camera sensor is connected, and using python and computer vision with some image processing techniques, the beam balanced.

#### In this repo, you can find the hardware design folder which contains all the Solidworks parts and assembly. In the open loops tests folder, you will find some python codes for applying image processing techniques on the captured images. In the closed loop folder, you will find the python codes for using the PID control on the raspberry pi. All technical detalis can be dound in the project report folder.
