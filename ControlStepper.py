import serial
import math
import time
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
    time.sleep(1)
    print(arduino.readline())

MoveMotor(10000, 0, 'COM8')

# arduino1 = serial.Serial(port='COM4', baudrate=115200, timeout=0.1)
# arduino1.write("001000001000/n".encode('utf-8'))
# print(arduino1.readline())
