import datetime
from ESP32RestSerialAPI import ESP32Client
from skimage.registration import phase_cross_correlation
import urllib.request
import urllib
import cv2
import numpy as np
import time
from pymba import Vimba
import matplotlib.pyplot as plt
import h5py
import serial
import math

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

def MoveMotor(Xsteps, Ysteps, Com, baudrate=115200, timeout=0.5):
    b = list("000000000000")

    Xsteps = Xsteps
    Ysteps = Ysteps

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
    #print(b1)

    arduino = serial.Serial(port=Com, baudrate=baudrate, timeout=timeout)
    arduino.write(b1.encode())
    time.sleep(max(1 + (abs(Xsteps) // 1000), 1 + (abs(Ysteps) // 1000), 1.5))
    print(arduino.readline())

'''
def MoveMotor(X_step, Y_step, Motor):
    # if np.abs(X_step) < 1500 or np.abs(Y_step) < 1500:
    #     if X_step == 0:
    #         Reverse_X_Step = 0
    #     else:
    #         Reverse_X_Step = -np.sign(X_step) * 1500
    #     if Y_step == 0:
    #         Reverse_Y_Step = 0
    #     else:
    #         Reverse_Y_Step = -np.sign(Y_step) * 1500
    #
    #     if (Reverse_Y_Step != 0 or Reverse_X_Step != 0):
    #         Motor.move_stepper(steps=(Reverse_X_Step, Reverse_Y_Step, 0), speed=200, is_absolute=False,
    #                            is_blocking=True)
    #         time.sleep(2)
    #         Motor.move_stepper(steps=(X_step - Reverse_X_Step, Y_step - Reverse_Y_Step, 0), speed=200,
    #                            is_absolute=False, is_blocking=True)
    #         time.sleep(max(2 + (X_step // 1000), (1 + Y_step) // 1000, 2))
    #
    # else:
    #     Motor.move_stepper(steps=(X_step, Y_step, 0), speed=200, is_absolute=False,
    #                        is_blocking=True)
    #     time.sleep(max(1 + (X_step // 1000), 1 + (Y_step // 1000), 2))
    Motor.move_stepper(steps=(X_step, Y_step, 0), speed=200, is_absolute=False,
                       is_blocking=True)
    time.sleep(max(1 + (abs(X_step) // 900), 1 + (abs(Y_step) // 900), 2))
'''

serialport1 = 'COM8'
#Motor = ESP32Client(serialport=serialport1)

# We acquire images from the other camera though Mobilehotspot connection
url = 'http://192.168.137.61/cam-hi.jpg'

#create the hf file to save the output
TodaysDate = datetime.date.today()
d1 = TodaysDate.strftime("%d_%m_%Y_")

CurrentTime = datetime.datetime.now()
t1 = CurrentTime.strftime("%H_%M_%S")

hdf = h5py.File('hdf5Data/' + d1 + t1 + '.hdf5', 'w')

#saving the fixed parameters i nthe hdf5
hdf.create_dataset('zo', data=13e-3) #the distance between the object and the detector in meter //41.5e-3
hdf.create_dataset('dxd', data=3.45e-6) #the size of the detector pixel in meter
hdf.create_dataset('wavelength', data=450e-9) #the wavelength of the
hdf.create_dataset('entrancePupilDiameter', data=0.5e-3) #entrancePupilDiameter, 1.587e-3

#The positions for Pty
#Data = np.loadtxt("UC2_PtychCoords.txt", dtype=float)
Data = np.loadtxt("0.1Spiral200.txt", dtype=float)

#import within a known radius
radii = np.hypot(Data[:, 0], Data[:, 1])
Data = Data[radii < 0.9] #Get the closest 50 points to the center  193
# radii_sorted = np.sort(radii)
#plt.plot(radii_sorted[:50])

plt.scatter(*zip(*Data), color='blue', label='measured-positions')
plt.show()

Current_Position_X,  Current_Position_Y = 0, 0

X_step = 0
Y_step = 0

background = []
#measured_positions = []
encoder = []
encoder_images = []
ptychogram = []
SquareCaptionOrder = 0

#try:
with Vimba() as vimba:
    camera = vimba.camera(0)
    print(camera)
    camera.open()
    camera.arm('SingleFrame')
    exposure_time = camera.ExposureTime
    #camera.ExposureTime.set(1727e-6)
    print('exposure_time = ', exposure_time)
    # get a copy of the frame data
    frame = camera.acquire_frame()
    image1 = frame.buffer_data_numpy()
    #camera.close()

    #snap a square around the center
    MinShape = np.min(image1.shape)
    MaxShape = np.max(image1.shape)
    shape1 = image1.shape[1]

    '''
    if MinShape == image1.shape[0]:
        image = image1[:, (MaxShape-MinShape)//2:(MaxShape+MinShape)//2]
        SquareCaptionOrder = 1
    elif MinShape == image1.shape[1]:
        image = image1[(MaxShape - MinShape)//2:(MaxShape + MinShape)//2, :]
        SquareCaptionOrder = 2
    else:
        image = image1
    '''

    image = image1[150:image1.shape[0]-270, 180:image1.shape[1]-608]
    #image = image1[0:(MaxShape + MinShape) // 2 - 300, 200:(MaxShape + MinShape) // 2 - 100]
    #image = image1[200:(MaxShape + MinShape) // 2 - 200, 250:(MaxShape + MinShape) // 2 - 150]  # (MaxShape - MinShape)//2

    hdf.create_dataset('Nd', data=image.shape[0]*image.shape[1])  # number of the detector pixels

    # convert colour space if desired

    #exposure_time
    #time = exposure_time.get()
    #inc = exposure_time.get_increment()
    #exposure_time.set(time + inc)
    hdf.create_dataset('exposure_times', data=exposure_time)  # the wavelength of the

    #Motor.move_stepper(steps=(1000, 1000, 0), speed=150, is_absolute=False,is_blocking=True)
    MoveMotor(1000, 1000, serialport1)
    time.sleep(1)
    # Motor.move_stepper(steps=(-1000, -1000, 0), speed=150, is_absolute=False,
    #                    is_blocking=True)

    '''
    try:
        image = cv2.cvtColor(image, PIXEL_FORMATS_CONVERSIONS[frame.pixel_format])
    except KeyError:
        pass
    '''

    M = 0

    # taking images without the illumination source
    # for now we cannot control the laser autmatically
    # we take those images in different positions and turn the Laser on once we're done

    #print('recording background images, please turn the Laser off')
    BackgroundSteps = [(1000, 0, 0), (0, 1000, 0), (-1000, 0, 0), (-1000, 0, 0), (0, -1000, 0),
                       (0, -1000, 0), (1000, 0, 0), (1000, 0, 0), (-1000, 1000, 0)]
    background.append(image)
    i = 0
    print('recording background images, please turn off the Laser, once it is off, please enter 1')
    LaserOn = input('enter any input to continue.\n')
    for j, step in enumerate(BackgroundSteps):
        #Motor.move_stepper(steps=step, speed=200, is_absolute=False, is_blocking=True)
        MoveMotor(step[0], step[1], serialport1)

        # get a copy of the frame data

        camera.new_frame()
        frame11 = camera.acquire_frame()
        image11 = frame11.buffer_data_numpy()

        #camera.close()
        '''
        if SquareCaptionOrder == 1:
            image = image11[:, (MaxShape - MinShape) // 2:(MaxShape + MinShape) // 2]
        elif SquareCaptionOrder == 2:
            image = image11[(MaxShape - MinShape) // 2:(MaxShape + MinShape) // 2, :]
        else:
            image = image11
        '''

        image = image11[150:image11.shape[0]-270, 180:image11.shape[1]-608]
        #image = image11[0:(MaxShape + MinShape) // 2 - 300, 200:(MaxShape + MinShape) // 2 - 100]
        #image = image11[200:(MaxShape + MinShape) // 2 - 200, 250:(MaxShape + MinShape) // 2 - 150]  # (MaxShape - MinShape)//2
        print('image = ' + str(np.average(image)))
        background.append(image.copy())
        print('background' + str(i) + str(np.average(background[i])))
        i = i + 1
        #cv2.imshow('Captured_Frame', image)
        #cv2.waitKey()

    print('recording background images is done, please turn the Laser on, once it is on, please enter 1')
    LaserOn = input('enter any input to continue.\n')
    hdf.create_dataset('background', data=background)  # Background images
    time.sleep(1)

    encoder_frame = capture_frame(url)
    OriginalEncoderImage = encoder_frame
    encoder_images.append(OriginalEncoderImage)
    ptychogram.append(image)
    encoder.append([0, 0])

    #initial positions
    a01 = 0
    a00 = 0

    #initial shift
    Xshift = 0
    Yshift = 0

    #pixel shift per step factor,
    y_factor_pixel_to_steps = -0.02975 #-0.0185  #-0.013679 #-0.021
    x_factor_pixel_to_steps = -0.02702 #0.0204#0.0184

    #convert the shift to a distance in meter
    #DistancePerPixel = 4.56e-6
    DistancePerPixel = 5e-6#4.03e-6

    #coordinates to shifts factor (controls the FOV)
    #Coordinates in mm to shift in pixels

    CoToShift = DistancePerPixel*1000   #Coordinates are in mm DistancePerPixel is in um/pixel

    #2 better for less overlapping ratio

    #steps to shifts  factors
    y_factor = CoToShift*y_factor_pixel_to_steps
    x_factor = CoToShift*x_factor_pixel_to_steps

    #5000 steps max in each direction almost equal to #200/0.0113 * 3
    #y_factor = -1/25
    #x_factor = 1/25
    cnt = 1
    for a in Data:
        #cv2.imwrite("CompleteSet/%s_%s_%s.jpg" % (str(M), str(round(Current_Position_X, 3)),
                                                 # str(round(Current_Position_Y, 3))), image)
        M = M + 1
        Y_step = (a[0] - a00) //y_factor #the steps number to get to the new position = new position - previous position
        X_step = (a[1] - a01) //x_factor #  shift[1]*8.9976 #update it iteratively
        # #flipping the coordinates
        # Y_step = (a[1] - a01) // y_factor
        # X_step = (a[0] - a00) // x_factor
        print(a[0], a[1])
        print("steps before loop ", Y_step, X_step)
        #MoveMotor(X_step, Y_step, Motor)
        MoveMotor(int(X_step), int(Y_step), serialport1)

        #we need the new and the previous cords that's why we save the current ones before new iteration
        a00 = a[0]
        a01 = a[1]

        #we measure the shift after movement
        #cv2.imshow(encoder_frame)
        encoder_frame = capture_frame(url)
        encoder_images.append(encoder_frame.copy())
        shift, error, diffphase = find_shift_based_on_gradient(OriginalEncoderImage, encoder_frame)
        print("shift before loop ", shift[1], shift[0])

        # #if the point is out of FOV, we skip it and go to the next one
        # if (np.abs(a[0]/CoToShift - shift[0]) > 0.5*np.abs(a[0]/CoToShift) or
        #         np.abs(a[1]/CoToShift - shift[1]) > 0.5*np.abs(a[1]/CoToShift)):
        #     MoveMotor(-X_step, -Y_step, Motor)
        #     continue
        #feedback loop to get to the expected position, normal coordinates

        cnt1 = 0
        while (np.abs(a[0]/CoToShift - shift[1]) > 1.5 or np.abs(a[1]/CoToShift - shift[0]) > 1.5) and cnt1 < 5:
            cnt1 = cnt1 + 1
            if np.abs(a[0]/CoToShift - shift[1]) <= 1.5:
                feedback_Y_Steps = 0
            else:
                feedback_Y_Steps = (a[0]/CoToShift - shift[1]) // y_factor_pixel_to_steps
            if np.abs(a[1]/CoToShift - shift[0]) <= 1.5:
                feedback_X_Steps = 0
            else:
                feedback_X_Steps = (a[1]/CoToShift - shift[0]) // x_factor_pixel_to_steps
            #MoveMotor(feedback_X_Steps, feedback_Y_Steps, Motor)
            print("steps", feedback_X_Steps, feedback_Y_Steps)
            MoveMotor(int(feedback_X_Steps), int(feedback_Y_Steps), serialport1)

            #Motor.move_stepper(steps=(feedback_X_Steps, feedback_Y_Steps, 0), speed=125, is_absolute=False,
               #                is_blocking=True)
            #time.sleep(1)

            encoder_frame = capture_frame(url)
            shift, error, diffphase = find_shift_based_on_gradient(OriginalEncoderImage, encoder_frame)

            print("Shift: " + str(shift))
            print("X_expected   " + str(a[1]/CoToShift))
            print("Y_expected  " + str(a[0]/CoToShift))

        '''
        # update the y and x factor
        if Y_step != 0:
            y_factor = -2 * np.abs((shift[0] - Yshift) / Y_step)
            print('y_factor = ', y_factor)
        if X_step != 0:
            x_factor = 2 * np.abs((shift[1] - Xshift) / X_step)
            print('Xfactor = ', x_factor)
        '''

        '''
        #feedback loop to get to the expected position, flipped coordinates
        while (np.abs(a[0]/CoToShift - shift[1]) > 3 or np.abs(a[1]/CoToShift - shift[0]) > 3):
            if np.abs(a[1]/CoToShift - shift[0]) <= 3:
                feedback_Y_Steps = 0
            else:
                feedback_Y_Steps = (a[1]/CoToShift - shift[0]) // y_factor
            if np.abs(a[0]/CoToShift - shift[1]) <= 3:
                feedback_X_Steps = 0
            else:
                feedback_X_Steps = (a[0]/CoToShift - shift[1]) // x_factor
            MoveMotor(feedback_X_Steps, feedback_Y_Steps, Motor)
            #Motor.move_stepper(steps=(feedback_X_Steps, feedback_Y_Steps, 0), speed=125, is_absolute=False,
               #                is_blocking=True)
            #time.sleep(1)

            encoder_frame = capture_frame(url)
            shift, error, diffphase = find_shift_based_on_gradient(OriginalEncoderImage, encoder_frame)

            print("Shift: " + str(shift))
            print("X_expected   " + str(a[0]/CoToShift))
            print("Y_expected  " + str(a[1]/CoToShift))
        '''

        Xshift = shift[0]
        Yshift = shift[1]

        encoder_images.append(encoder_frame.copy())
        encoder.append([shift[1]*DistancePerPixel, shift[0]*DistancePerPixel])  #4.46e-6 is um per pixel

        print('recording Ptychogram' + str(cnt))
        cnt = cnt + 1
        # print("Shift: " + str(shift))
        # print("X_expected   " + str(a[1]/CoToShift))
        # print("Y_expected  " + str(a[0]/CoToShift))

        # get a copy of the frame data
        camera.new_frame()
        frame2 = camera.acquire_frame()
        image21 = frame2.buffer_data_numpy()
        # convert colour space if desired
        #capture a square array around the center

        '''
        if SquareCaptionOrder == 1:
            image22 = image21[:, (MaxShape - MinShape) // 2:(MaxShape + MinShape) // 2]
        elif SquareCaptionOrder == 2:
            image22 = image21[(MaxShape - MinShape) // 2:(MaxShape + MinShape) // 2, :]
        else:
            image22 = image21
        '''

        #image22 = image21[200:(MaxShape + MinShape) // 2 - 200, 250:(MaxShape + MinShape) // 2 - 150]  # (MaxShape - MinShape)//2
        #image22 = image21[0:(MaxShape + MinShape) // 2 - 300, 200:(MaxShape + MinShape) // 2 - 100]
        image22 = image21[150:image21.shape[0]-270, 180:image21.shape[1]-608]
        ptychogram.append(image22.copy())

        '''
        ax[0].imshow(image[::4,::4], interpolation='nearest')
        ax[0].set_title('diffraction pattern @ (%0.2f, %0.2f) micro meter' % (shift[1]*5.78, shift[0]*5.78))

        ax[1].imshow(encoder_frame[::4,::4], interpolation='nearest')
        ax[1].set_title('encoder image @ (%0.2f, %0.2f) micro meter' % (shift[1]*5.78, shift[0]*5.78))

        # drawing updated values
        fig1.canvas.draw()

        # This will run the GUI event
        # loop until all UI events
        # currently waiting have been processed
        #fig1.canvas.flush_events()

        time.sleep(3)
        #measured_positions.append((Current_Position_X, Current_Position_Y))
        '''

        #Current_Position_X = Current_Position_X + shift[1]
        #Current_Position_Y = Current_Position_Y - shift[0]

#plt.savefig('positions.png')
hdf.create_dataset('encoder', data=encoder)  # Background images
hdf.create_dataset('ptychogram', data=ptychogram)  # Background images
hdf.create_dataset('encoderImages', data=encoder_images)  # Background images

#except:
#np.savez('positions.npz', measured_positions=encoder, ptychogram=ptychogram, encoder_images=encoder_images)
plt.scatter(*zip(*encoder), color='blue', label='measured-positions')
plt.show()