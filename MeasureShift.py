
import datetime
from ESP32RestSerialAPI import ESP32Client
from skimage.registration import phase_cross_correlation
import urllib.request
import urllib
import cv2
import numpy as np
import time
import serial
import math
import pandas as pd

def MoveMotor(Xsteps, Ysteps, Com, baudrate=115200, timeout=0.5):
    b = list("000000000000")

    Xsteps = Xsteps
    Ysteps = Ysteps

    print(b)
    if Xsteps < 0:
        b[0] = '1'

    if Ysteps < 0:
        b[6] = '1'

    AbsX = abs(Xsteps)
    AbsY = abs(Ysteps)

    b[5-int(math.log10(AbsX + 0.001)):6] = str(AbsX)
    b[11-int(math.log10(AbsY + 0.001)):12] = str(AbsY)
    #a[1],

    b1 = ''.join(b) + 'd' #+ '\r\n'
    print(b1)

    arduino = serial.Serial(port=Com, baudrate=baudrate, timeout=timeout)
    arduino.write(b1.encode())
    time.sleep(max(1 + (abs(Xsteps) // 1500), 1 + (abs(Ysteps) // 1500), 2))
    print(arduino.readline())

#PIXEL_FORMATS_CONVERSIONS = {'BayerRG8': cv2.COLOR_BAYER_RG2RGB,}
def find_shift_based_on_gradient(img1, img2):
    I1_y, I1_x = np.gradient(img1, axis=(-2, -1))
    I2_y, I2_x = np.gradient(img2, axis=(-2, -1))
    I1 = I1_y + 1j * I1_x
    I2 = I2_y + 1j * I2_x
    shifts, err, phase_diff = phase_cross_correlation(I1, I2, upsample_factor=10)
    return shifts, err, phase_diff

#capture the frame for the other camera, positioning camera
def capture_frame(url):
    imgResp = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
    img = cv2.imdecode(imgNp, -1)
    return img

'''
def MoveMotor(X_step, Y_step, Motor):
    # if np.abs(X_step) < 1500 or np.abs(Y_step) < 1500:
    #     Reverse_Y_Step = 0
    #     Reverse_X_Step = 0
    #     if X_step == 0:
    #         Reverse_X_Step = 0
    #     elif abs(X_step) < 1500:
    #         Reverse_X_Step = -np.sign(X_step) * 1500
    #     if Y_step == 0:
    #         Reverse_Y_Step = 0
    #     elif abs(Y_step) < 1500:
    #         Reverse_Y_Step = -np.sign(Y_step) * 1500
    #
    #     if (Reverse_Y_Step != 0 or Reverse_X_Step != 0):
    #         Motor.move_stepper(steps=(Reverse_X_Step, Reverse_Y_Step, 0), speed=200, is_absolute=False,
    #                            is_blocking=True)
    #         time.sleep(2)
    #         Motor.move_stepper(steps=(X_step - Reverse_X_Step, Y_step - Reverse_Y_Step, 0), speed=200,
    #                            is_absolute=False, is_blocking=True)
    #         time.sleep(max(2 + (X_step // 1000), (1 + Y_step) // 1000, 2))

    #else:
    Motor.move_stepper(steps=(X_step, Y_step, 0), speed=200, is_absolute=False,
                       is_blocking=True)
    time.sleep(max(1 + (abs(X_step) // 1000), 1 + (abs(Y_step) // 1000), 2))
'''

serialport1 = 'COM8'
#Motor = ESP32Client(serialport=serialport1)

# We acquire images from the other camera though Mobilehotspot connection
url = 'http://192.168.137.61/cam-hi.jpg'

encoder_frame = capture_frame(url)
OriginalEncoderImage = encoder_frame

#MoveMotor(0, 5000, Motor)
MoveMotor(7500, 0, serialport1)

encoder_frame = capture_frame(url)
shift, error, diffphase = find_shift_based_on_gradient(OriginalEncoderImage, encoder_frame)
print(shift)
kjkjjjj
OriginalEncoderImage = capture_frame(url)
MoveMotor(-13000, 0, Motor)

encoder_frame = capture_frame(url)
shift, error, diffphase = find_shift_based_on_gradient(OriginalEncoderImage, encoder_frame)

print('xsteps -16000', shift)


OriginalEncoderImage = capture_frame(url)
MoveMotor(-13000, 0, Motor)

encoder_frame = capture_frame(url)
shift, error, diffphase = find_shift_based_on_gradient(OriginalEncoderImage, encoder_frame)

print('xsteps -16000', shift)

OriginalEncoderImage = capture_frame(url)
MoveMotor(13000, 0, Motor)

encoder_frame = capture_frame(url)
shift, error, diffphase = find_shift_based_on_gradient(OriginalEncoderImage, encoder_frame)

print('xsteps +16000', shift)


'''
x_Steps = {0: 0}
x_Shift = {0: 0}
Y_Steps = {0: 0}
Y_Shift = {0: 0}
measured = {0: 0}
expected = {0: 0}
dct = {'x-steps': x_Steps, 'x-shift': x_Shift, 'y-steps': Y_Steps, 'y-shift': Y_Shift}

# forming dataframe
data = pd.DataFrame(dct)
Y_slope = -0.0112
X_slope = 0.0112
# storing into the excel file
data.to_excel("StepsShiftsData.xlsx")
Current_Position_X,  Current_Position_Y = 0, 0
expected_Position_X, expected_Position_Y = 0, 0

#with open('MovementCalb.txt', 'w') as f:
#f.write("phase_cross_correlation \n")
#f.write("steps, shift, error, diffphase \n")


M = 0
epsilon = 6e-9

from scipy import ndimage
MovingSteps = [# first data around x = 0
               (0, 100, 0), (0, -100, 0), (0, 200, 0), (0, 300, 0), (0, 500, 0), (0, 1000, 0),
                (0, 2000, 0), (0, 5000, 0), (0, -10000, 0), (0, 15000, 0), (0, -15000, 0)
               #(1000, 0, 0), (-1050, 0, 0), # x=-50
                #(1050, 0, 0), (-1100, 0, 0), # x=-100
                ]

MovingSteps2 = [# first data around x = 0
                (100, 0, 0), (200, 0, 0), (300, 0, 0), (500, 0, 0), (1000, 0, 0), (2000, 0, 0), (5000, 0, 0),
                (-10000, 0, 0), (15000, 0, 0), (-15000, 0, 0)
               #(1000, 0, 0), (-1050, 0, 0), # x=-50
                #(1050, 0, 0), (-1100, 0, 0), # x=-100
                ]

frame0 = capture_frame(url)

for Mstep in MovingSteps:
    print("steps: " + str(Mstep))
    Motor.move_stepper(Mstep, speed=200, is_absolute=False,
                       is_blocking=True)
    time.sleep(max(1 + (abs(Mstep[0]) // 900), 1 + (abs(Mstep[1]) // 900), 2))

    frame1 = capture_frame(url)
    shift, error, diffphase = find_shift_based_on_gradient(frame0, frame1)
    print("Shift: " + str(shift))

    Current_Position_X = Current_Position_X + shift[1]
    Current_Position_Y = Current_Position_Y - shift[0]


    x_Steps[M] = Mstep[0]
    x_Shift[M] = shift[1]
    Y_Steps[M] = Mstep[1]
    Y_Shift[M] = shift[0]
    measured[M] = (Current_Position_X, Current_Position_Y)
    expected[M] = (expected_Position_X, expected_Position_Y)
    M = M + 1




for Mstep in MovingSteps2:
    print("steps: " + str(Mstep))
    Motor.move_stepper(Mstep, speed=200, is_absolute=False,
                       is_blocking=True)
    time.sleep(max(1 + (abs(Mstep[0]) // 900), 1 + (abs(Mstep[1]) // 900), 2))

    frame1 = capture_frame(url)
    shift, error, diffphase = find_shift_based_on_gradient(frame0, frame1)
    print("Shift: " + str(shift))

    Current_Position_X = Current_Position_X + shift[1]
    Current_Position_Y = Current_Position_Y - shift[0]


    x_Steps[M] = Mstep[0]
    x_Shift[M] = shift[1]
    Y_Steps[M] = Mstep[1]
    Y_Shift[M] = shift[0]
    measured[M] = (Current_Position_X, Current_Position_Y)
    expected[M] = (expected_Position_X, expected_Position_Y)
    M = M + 1

#measured_positions.append((Mstep, shift, error, diffphase))
#f.write("x shift %s:%s _ y shift %s %s" % (str(Mstep[0]), str(shift[1]), str(Mstep[1]), str(shift[0])) + "\n")
#f.write(str(Mstep) + str(shift) + str(error) + str(diffphase) + "\n")

        #save data to excel file
dct = {'x-steps': x_Steps, 'x-shift': x_Shift, 'y-steps': Y_Steps, 'y-shift': Y_Shift,
       'measured': measured, 'expected': expected}

# forming dataframe
data = pd.DataFrame(dct)

# storing into the excel file
data.to_excel("NewStepsShiftsData.xlsx")

'''
