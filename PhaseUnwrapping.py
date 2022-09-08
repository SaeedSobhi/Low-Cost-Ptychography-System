#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 13:29:38 2022
@author: friedrichvonsaxon
"""

import h5py
import napari
import matplotlib.pyplot as plt
import numpy as np
import cv2

from mpl_toolkits.axes_grid1 import make_axes_locatable

f632 = 'Reconstructed/10_06_2022_13_26_53_Reconstructed.hdf5'#'example_data/04032022_printed_sample_4npsm.hdf5'
Uc2Obj = 'hdf5Data/04032022_printed_sample_4npsm.hdf5'
f631 = 'Reconstructed/New/ResolutionTargetReconstructed040822.hdf5'
f632 = 'Reconstructed/10_06_2022_13_26_53_Reconstructed.hdf5'
'''
f632 = h5py.File('04032022_printed_sample_4npsm.hdf5','r')
fList = list(f632.keys())
a = f632[fList[0]]
'''

with h5py.File(f632, 'r') as hf:
    obj = hf.get('object')[()]
    obj1 = hf.get('probe')[()]
    pixel_size = hf.get('dxp')[()]
    w = hf.get('wavelength')[()]

with h5py.File(f631, 'r') as hf:
    obj2 = hf.get('object')[()]
    obj21 = hf.get('probe')[()]
    pixel_size = hf.get('dxp')[()]
    w = hf.get('wavelength')[()]
'''
with h5py.File(Uc2Obj, 'r') as hf:
    obj2 = hf.get('object')[()]
    obj21 = hf.get('probe')[()]
    pixel_size2 = hf.get('dxp')[()]
    w2 = hf.get('wavelength')[()]
'''

print(obj.shape)
pic = obj[-1, -1, -1, -1, :, :] #2700:3050, 2400:2750
pic2 = obj2[-1, -1, -1, -1, 800:2000, 900:2100]
# find the circles automatically
pic2 = pic2 + 1
output1 = np.abs(pic)
output2 = np.abs(pic2)
plt.figure(1)
plt.imshow(output1, cmap=plt.gray())
plt.figure(2)

plt.imshow(output2, cmap=plt.gray())
plt.show()
errerr
'''
output1 = np.abs(pic) 
plt.imshow(output, cmap=plt.gray())
plt.show()
output = np.zeros(output1.shape, int)
for i in range(0, output1.shape[0]):
    for j in range(0, output1.shape[1]):
        output[i, j] = int(output1[i, j])
print(output)

plt.imshow(output, cmap=plt.gray())
plt.show()

#cv2.imshow('int output', output)
#cv2.waitKey(5)
#gray = cv2.cvtColor(np.real(output), cv2.COLOR_BGR2GRAY)

# detect circles in the image
circles = cv2.HoughCircles(output, cv2.HOUGH_GRADIENT, 0.5, 50)
# ensure at least some circles were found
if circles is not None:
	# convert the (x, y) coordinates and radius of the circles to integers
	circles = np.round(circles[0, :]).astype("int")
	# loop over the (x, y) coordinates and radius of the circles
	for (x, y, r) in circles:
		# draw the circle in the output image, then draw a rectangle
		# corresponding to the center of the circle
		cv2.circle(output, (x, y), r, (0, 255, 0), 4)
		cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

	# show the output image
	cv2.imshow("output", np.hstack([pic, output]))
	cv2.waitKey(0)

plt.imshow(np.angle(pic), cmap=plt.hsv())
plt.show()
'''
pic22 = obj2[-1, -1, -1, -1, :, :] #2700:3050, 2400:2750


#cv2.imwrite('pic2.jpg', pic)
pic2 = obj[0, 0, 0, 0, 1:500, 1:500]
pic3 = obj[0, 0, 0, 0, 500:1000, 500:1000]
pic1 = obj1[0, 0, 0, 0, :, :]

#%%%%
from skimage.restoration import unwrap_phase

image_unwrapped = unwrap_phase(np.angle(pic))
image_unwrapped1 = image_unwrapped  #unwrap_phase(pic1)

fig, ax = plt.subplots(1, 2, figsize=(16, 9))

# plt.plot(phase1)
ax[0].imshow(np.angle(pic22), cmap=None)
ax[0].set_title("UC2 reconstructed")

#ax[0, 1].imshow(np.abs(pic), cmap=plt.gray())
#ax[0, 1].set_title("Daniels's Pty setup")

#ax[1, 0].imshow(np.angle(pic22[2850:3000, 2750:3000]), cmap=plt.hsv())
#[1, 0].set_title("focused area, UC2")

ax[1].imshow(np.angle(pic[2850:3000, 2750:3000]), cmap=None)
ax[1].set_title("focused area, Daniel's Pty setup")
plt.show()

#



#cv2.imwrite('pic.jpg', np.real(obj[0, 0, 0, 0, :,:]))
#cv2.imwrite('pic1.jpg', pic1)
#print(np.angle(pic))

#plt.imshow(np.angle(pic[400:800, 500:800]), cmap=plt.hsv())
#plt.show()

centery = 465
centerx = 558

#wrapped_sample = np.angle(pic[(centery - 30):(centery + 30), (centerx - 30):(centerx + 30)])
#unwrapped_sample = image_unwrapped[(centery-30):(centery+30), (centerx-30):(centerx+30)]
'''
fig, ax = plt.subplots()

cax = ax.imshow(np.angle(pic[0:800, 0:800]), cmap=plt.hsv())

cbar = fig.colorbar(cax, ticks=[-np.pi+0.01, 0, np.pi-0.01])
cbar.ax.set_yticklabels(['-\u03C0', '0', '\u03C0'])  # vertically oriented colorbar

#plt.imshow(wrapped_sample, cmap=plt.hsv(), interpolation='nearest', label="scale 1:1.4\u03BCM")
plt.title("scale 230\u03BCm:100 steps")
plt.show()
'''

#plt.imshow(np.real(obj[0, 0, 0, 0, :, :]), cmap=plt.gray())
#plt.show()

#del obj
#del obj1
#del pic
#del pic1

#%%%%
#viewer = napari.view_image(image_unwrapped, colormap='magma')
#viewer.add_image(image_unwrapped1, name='astronaut')
#%%%%%%

#phase1 = image_unwrapped[274,22:83]
'''
Centers = [(465, 558), (535, 557), (604, 554), (675, 552), (466, 629), (468, 698)]

for (centery, centerx) in Centers:

    #centery = 465
    #centerx = 558

    wrapped_sample = np.angle(pic[(centery-30):(centery+30), (centerx-30):(centerx+30)])
    unwrapped_sample = image_unwrapped[(centery-30):(centery+30), (centerx-30):(centerx+30)]

    wrapped_phase_along_Xaxis = np.angle(pic[centery, (centerx-30):(centerx+30)])
    unwrapped_phase_along_Xaxis = image_unwrapped[centery, (centerx-30):(centerx+30)]

    wrapped_phase_along_Yaxis = np.angle(pic[(centery-30):(centery+30), centerx])
    unwrapped_phase_along_Yaxis = image_unwrapped[(centery-30):(centery+30), centerx]

    fig, axs = plt.subplots(2, 3, figsize=(16, 9))

    #axs[0, 0].imshow(wrapped_sample, cmap=plt.hsv(), interpolation='nearest')
    axs[0, 0].set_title("wrapped_sample")

    #plt.sca(axs[0, 0])
    #plt.yticks(np.arange(-np.pi, np.pi, np.pi/3))

    #axs[0, 0].imshow(wrapped_sample, cmap=plt.hsv(), interpolation='nearest')
    #['$-\u03C0$','$0$','$\u03C0$']):

    #divider = make_axes_locatable(axs[0, 0])
    #cax = divider.append_axes('right', size='5%', pad=0.05)

    cax = axs[0,0].imshow(wrapped_sample, cmap=plt.hsv(), interpolation='nearest')

    #cbar = fig.colorbar(cax, ticks=[-np.pi + 0.01, 0, np.pi - 0.01])
    #cbar.ax.set_yticklabels(['-\u03C0', '0', '\u03C0'])  # vertically oriented colorbar
    #cbar = fig.colorbar(cax)
    #cbar.axs[0, 0].set_yticklabels(['-\u03C0', 0, '\u03C0'])
    axs[1, 0].imshow(unwrapped_sample, cmap=plt.hsv(), interpolation='nearest')
    axs[1, 0].set_title("unwrapped_sample")

    ##
    axs[0, 1].plot(wrapped_phase_along_Xaxis)
    axs[0, 1].set_title('Wrapped Phase along x through the center')
    axs[0, 1].set_ylabel('rad')
    #axs[0, 1].yaxis.set_ticks(['$-\u03C0$','$0$','$\u03C0$'])

    axs[1, 1].plot(unwrapped_phase_along_Xaxis)
    axs[1, 1].set_title("Unwrapped Phase along x through the center")
    axs[1, 1].set_ylabel('rad')
    ##
    axs[0, 2].plot(wrapped_phase_along_Yaxis)
    axs[0, 2].set_title('Wrapped Phase along y through the center')
    axs[0, 2].set_ylabel('rad')
    #axs[0, 2].yaxis.set_ticks(['$-\u03C0$', '$0$', '$\u03C0$'])#np.arange(-np.pi, np.pi, np.pi/2))

    axs[1, 2].plot(unwrapped_phase_along_Yaxis)
    axs[1, 2].set_title("Unwrapped Phase along y through the center")
    axs[1, 2].set_ylabel('rad')

    #plt.plot(phase1)
    plt.show()

'''

'''
centers = [[274, 52], [276, 123], [278, 193], [279, 263]]
d = 0
for i in range(int(np.size(centers)/2)-1):
    d = d+(centers[i+1][1]-centers[i][1])
d = d/(int(np.size(centers)/2)-1)
l = 160
lPerPix = l/d
r = 70 # um

dataPointsM = [-65, -55, -45, -35, -25, -15, -5]

dataPointsM1 = np.round(np.array(dataPointsM)/lPerPix)
dataPointsM1 = centerx + dataPointsM1
phases1 = np.zeros(np.size(dataPointsM1))
for i in range(np.size(dataPointsM1)):
    phases1[i] = image_unwrapped[centery, int(dataPointsM1[i])]

phaseDifferenceM1 = phases1[1:-1] - phases1[0:-2]

dataPoints = np.array([5, 15, 25, 35, 45, 55, 65])

dataPointCoor = np.round(np.array(dataPoints)/lPerPix)
dataPointCoor = centerx + dataPointCoor
phases = np.zeros(np.size(dataPointCoor))
for i in range(np.size(dataPointCoor)):
    phases[i] = image_unwrapped[centery, int(dataPointCoor[i])]

phaseDifference = phases[0:-2] - phases[1:-1]
'''