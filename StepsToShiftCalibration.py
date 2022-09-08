from ESP32RestSerialAPI import ESP32Client
from skimage.registration import phase_cross_correlation
import urllib.request
import urllib
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
import pandas as pd
from openpyxl.workbook import Workbook
import serial
import math

def find_shift_based_on_gradient(img1, img2):
    I1_y, I1_x = np.gradient(img1, axis=(-2, -1))
    I2_y, I2_x = np.gradient(img2, axis=(-2, -1))
    I1 = I1_y + 1j * I1_x
    I2 = I2_y + 1j * I2_x
    shifts, err, phase_diff = phase_cross_correlation(I1, I2, upsample_factor=10)
    return shifts, err, phase_diff

def capture_frame(url):
    imgResp = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
    img = cv2.imdecode(imgNp, -1)
    return img

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

    b1 = ''.join(b) +'d' #+ '\r\n'
    print(b1)

    arduino = serial.Serial(port=Com, baudrate=baudrate, timeout=timeout)
    arduino.write(b1.encode())
    time.sleep(max(1 + (abs(Xsteps) // 1500), 1 + (abs(Ysteps) // 1500), 2))
    print(arduino.readline())

#perform a lateral shift in the x direction
serialport1 = 'COM8'

#Motor = ESP32Client(serialport=serialport1)

#.move_stepper((2000, 0, 0), speed=100, is_absolute=False, is_blocking=True)
#Motor.move_stepper(steps=(10, 0, 0), speed=100, is_absolute=False, is_blocking=True)

expected_positions = []
measured_positions = []
Steps = []
url = 'http://192.168.137.61/cam-hi.jpg'

from scipy import ndimage
MovingSteps = [(-2000, -2000, serialport1), (2000, 2000, serialport1), (-3000, -3000, serialport1),
               (3000, +3000, serialport1), (-5000, -5000, serialport1), (5000, 5000, serialport1),
               (-7000, -7000, serialport1), (7000, 7000, serialport1), (-9000, -9000, serialport1),
               (9000, 9000, serialport1), (-10000, 0, serialport1), (10000, 0, serialport1),
               (0, -10000, serialport1), (0, 10000, serialport1)]

MovingSteps2 = [# first data around x = 0
                (1900, 0, 0), (-1950, 0, 0), (1900, 0, 0), (-1950, 0, 0), (1900, 0, 0), (-1950, 0, 0), (1900, 0, 0),
                (-1950, 0, 0), (1900, 0, 0), (-1950, 0, 0), (1900, 0, 0), (-1950, 0, 0), (1900, 0, 0), (-1950, 0, 0),
               #(1000, 0, 0), (-1050, 0, 0), # x=-50
                #(1050, 0, 0), (-1100, 0, 0), # x=-100
                ]

'''
(1000, 0, 0), (-1100, 0, 0), (1150, 0, 0), (-1200, 0, 0), (1250, 0, 0), (-1300, 0, 0), (1350, 0, 0),
               (-1400, 0, 0), (1450, 0, 0), (-1500, 0, 0), (1550, 0, 0), (-1600, 0, 0), (1650, 0, 0), (-1700, 0, 0),
               (+1750, 0, 0), (-1800, 0, 0), (1850, 0, 0), (-1900, 0, 0), (1950, 0, 0), (-2000, 0, 0),
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

frame1 = capture_frame(url)
M = 0
epsilon = 6e-9
for Mstep in MovingSteps:
    expected_Position_X = Current_Position_X + Mstep[0] * X_slope
    expected_Position_Y = Current_Position_Y - Mstep[1] * Y_slope

    '''
    if np.abs(Mstep[0]) > 100:
        expected_Position_X = Current_Position_X + (Mstep[0] - np.sign(Mstep[0]) * 125) * 0.0146
    else:
        expected_Position_X = Current_Position_X + (Mstep[0]) * 0.0146
    if np.abs(Mstep[1]) > 100:
        expected_Position_Y = Current_Position_Y + (Mstep[1] - np.sign(Mstep[1]) * 125) * -0.0144
    else:
        expected_Position_Y = Current_Position_Y + (Mstep[1]) * -0.0144
    '''

    expected_positions.append((expected_Position_X, expected_Position_Y))

    frame0 = frame1
    print("steps: " + str(Mstep))
    MoveMotor(Mstep[0], Mstep[1], Mstep[2])
    #Motor.move_stepper(steps=Mstep, speed=200, is_absolute=False, is_blocking=True)
    time.sleep(3)

    frame1 = capture_frame(url)
    shift, error, diffphase = find_shift_based_on_gradient(frame0, frame1)
    print("Shift: " + str(shift))

    Current_Position_X = Current_Position_X + shift[1]
    Current_Position_Y = Current_Position_Y - shift[0]
    if Mstep[1] != 0:
        Y_slope = shift[0] / Mstep[1]
    if Mstep[0] != 0:
        X_slope = shift[1] / Mstep[0]

    measured_positions.append((Current_Position_X, Current_Position_Y))

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
data.to_excel("StepsShiftsData.xlsx")

#print(measured_positions)

fig, ax = plt.subplots()
ax.scatter(*zip(*measured_positions), color='blue', label='measured-positions')
ax.scatter(*zip(*expected_positions), color='red', label='expected-positions')

plt.show()





