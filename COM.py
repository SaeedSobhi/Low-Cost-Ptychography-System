from imageio import imread
import matplotlib.pyplot as plt
from pymba import Vimba
import numpy as np

import scipy.ndimage as ndi

def COMInfo(img):
    shape = img.shape
    x, y = shape[0] / 2, shape[1] / 2
    Xm, Ym = round(ndi.center_of_mass(img)[0], 2), round(ndi.center_of_mass(img)[1], 2)
    print("COM = (%d,%d), Center = (%d, %d)" % (Xm, Ym, x, y))

with Vimba() as vimba:
    camera = vimba.camera(0)
    print(camera)
    camera.open()
    camera.arm('SingleFrame')
    exposure_time = camera.ExposureTime
    #camera.ExposureTime.set(727e-6)
    print('exposure_time = ', exposure_time)
    # get a copy of the frame data
    frame = camera.acquire_frame()
    image1 = frame.buffer_data_numpy()
    MinShape = np.min(image1.shape)
    MaxShape = np.max(image1.shape)
    if MinShape == image1.shape[0]:
        image = image1[150:image1.shape[0]-270, 180:image1.shape[1]-608] # (MaxShape - MinShape)//2
        print(image.shape)
        SquareCaptionOrder = 1
    elif MinShape == image1.shape[1]:
        image = image1[0:(MaxShape + MinShape)//2, :]  #(MaxShape - MinShape)//2
        SquareCaptionOrder = 2
    else:
        image = image1

    plt.imshow(image, cmap=plt.gray())
    plt.show()


'''    
img = imread('origami.jpg',  pilmode="L")
#img1 = imread('origami.jpg')
shape = img.shape
x,y = shape[0]/2, shape[1]/2
Xm, Ym = round(ndi.center_of_mass(img)[0], 2), round(ndi.center_of_mass(img)[1], 2)
plt.imshow(img, cmap=plt.cm.gray, interpolation='nearest')
plt.show()
print("COM = (%d,%d), Center = (%d, %d)" % (Xm, Ym, x, y))
'''



