# importing modules
import urllib.request
import urllib
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
from skimage.feature import register_translation
from ESP32RestSerialAPI import ESP32Client
from skimage.registration import phase_cross_correlation

# 1. get an image from the calibration camera
url = 'http://192.168.137.102/cam-hi.jpg'

imgResp = urllib.request.urlopen(url)
imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
img = cv2.imdecode(imgNp, -1)

#perform a lateral shift in the x direction
serialport1 = 'COM7'
Motor = ESP32Client(serialport = serialport1)

time.sleep(3)
steps = 2000
Motor.move_stepper(steps=(10, 0, 0), speed=100, is_absolute=False, is_blocking=True)

Motor.move_stepper((2000, 0, 0), speed=100, is_absolute=False, is_blocking=True)
#Motor.move_stepper(axis=1, steps=-steps, speed=100, is_absolute=False, is_blocking=True)
print("Move in X, 2000")

#time.sleep(max(6, 3*steps//1000))

Motor.move_stepper((0, 2000, 0), speed=100, is_absolute=False, is_blocking=True)
#Motor.move_stepper(axis=2, steps=-steps, speed=100, is_absolute=False, is_blocking=True)
print("Move in y")
#time.sleep(max(6, 3*steps//1000))

Motor.move_stepper((-2000, 0, 0), speed=100, is_absolute=False, is_blocking=True)
#Motor.move_stepper(axis=1, steps=steps, speed=100, is_absolute=False, is_blocking=True)
print("Move in X")
#time.sleep(max(6, 3*steps//1000))

Motor.move_stepper((0, -2000, 0), speed=100, is_absolute=False, is_blocking=True)
#Motor.move_stepper(axis=2, steps=steps, speed=100, is_absolute=False, is_blocking=True)
#time.sleep(max(6, 3*steps//1000))
print("Move in y")

imgResp = urllib.request.urlopen(url)
imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
shifted_img = cv2.imdecode(imgNp, -1)

fig, axs = plt.subplots(1, 3, figsize=(16, 9))

axs[0].imshow(img, cmap=plt.gray(), interpolation='nearest')
axs[0].set_title("Orignial Image")

axs[1].imshow(shifted_img, cmap=plt.gray(), interpolation='nearest')
axs[1].set_title('Shifted Image')

# Show the output of a cross-correlation to show what the algorithm is
# doing behind the scenes
from skimage.registration import phase_cross_correlation
def find_shift_based_on_gradient(img1, img2):
    I1_y, I1_x = np.gradient(img1, axis=(-2, -1))
    I2_y, I2_x = np.gradient(img2, axis=(-2, -1))
    I1 = I1_y + 1j * I1_x
    I2 = I2_y + 1j * I2_x
    shifts, err, phase_diff = phase_cross_correlation(I1, I2, upsample_factor=10)
    print(shifts)
    return shifts

from scipy import ndimage
img = img.astype(np.float32)
shifts = find_shift_based_on_gradient(img[...,0], shifted_img[...,0])
im_diff = img[...,0] - ndimage.shift(shifted_img[...,0], shifts)

# image_product = np.fft.fft2(img) * np.fft.fft2(shifted_img).conj()
# cc_image = np.fft.fftshift(np.fft.ifft2(image_product))
# cc_image = np.abs(cc_image)
# NromalizedImage = cc_image / np.max(cc_image)
axs[2].imshow(im_diff)
axs[2].set_title('Cross-correlation')
plt.show()

# subpixel precision
shift, error, diffphase = phase_cross_correlation(img, shifted_img)
print("Detected pixel offset (y, x): {}".format(shift))

'''
print("Move in X")
Motor.move_stepper(axis=2, steps=1000, speed=100, is_absolute=False, is_blocking=True)
print("Move in Y")
time.sleep(3)
Motor.move_stepper(axis=1, steps=1000, speed=100, is_absolute=False, is_blocking=True)
print("Move in X")
time.sleep(3)
Motor.move_stepper(axis=2, steps=-1000, speed=100, is_absolute=False, is_blocking=True)
print("Move in Y")
time.sleep(3)
Motor.move_stepper(axis=1, steps=-1000, speed=100, is_absolute=False, is_blocking=True)

r = Motor.set_laser(channel='B', value=00000)
print(r)

#3. vimba readout
'''