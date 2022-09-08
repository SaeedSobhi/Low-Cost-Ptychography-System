import numpy as np
import h5py
import imageio
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker
import cv2

def shift_image(X, dx, dy):
    X = np.roll(X, -dy, axis=0)
    X = np.roll(X, int(-dx/4), axis=1)

    # M = np.float32([[1, 0, dx], [0, 1, dy]])
    # (rows, cols) = X.shape[:2]
    # X = cv2.warpAffine(X, M, (cols, rows))

    return X

hf = h5py.File('hdf5Data/05_08_2022_14_07_41.hdf5', 'r')

f632 = 'Reconstructed/10_06_2022_13_26_53_Reconstructed.hdf5'
print(hf.keys())

measured_Data = hf.get('encoder')
encoder_Images = hf.get('encoderImages')

image0 = encoder_Images[0]

shift25 = measured_Data[41]
image25 = encoder_Images[41]

RSimage25 = shift_image(image25, int(shift25[1]/5e-6), int(shift25[0]/5e-6))

print(shift25, shift25[0], shift25[1])

fig2, axs2 = plt.subplots(1, 3, figsize=(16, 9))

axs2[0].imshow(image0, cmap=plt.cm.gray, interpolation='nearest')
axs2[0].set_title("Original Image")

axs2[1].imshow(image25, cmap=plt.cm.gray, interpolation='nearest')
axs2[1].set_title("Shifted Image")

axs2[2].imshow(RSimage25, cmap=plt.cm.gray, interpolation='nearest')
axs2[2].set_title("shifted image after applying reverse shift")

plt.show()