import matplotlib.pyplot as plt
from imageio import imread
import numpy as np
import h5py
import scipy.ndimage as ndi

filename = 'PreProcessedPtychogramWithFIngerPrints.hdf5'
filepath = 'hdf5Data/'

hf = h5py.File(filepath+filename, 'r')
Ptycohgram = np.array(hf.get('ptychogram'))
NewPtychogram = []

def shift_image(X, dx, dy):
    X = np.roll(X, -dy, axis=0)
    X = np.roll(X, int(-dx/4), axis=1)

    # M = np.float32([[1, 0, dx], [0, 1, dy]])
    # (rows, cols) = X.shape[:2]
    # X = cv2.warpAffine(X, M, (cols, rows))

    return X

Y, X = Ptycohgram[1].shape[0]//2, Ptycohgram[1].shape[1]//2
for image in Ptycohgram:
    Ym, Xm = int(ndi.center_of_mass(image)[0]), int(ndi.center_of_mass(image)[1])
    centered_image = shift_image(image, Ym-Y, Xm-X)
    NewPtychogram.append(centered_image)
    # fig2, axs2 = plt.subplots(1, 2, figsize=(16, 16))
    #
    # axs2[0].imshow(image, cmap=plt.cm.gray, interpolation='nearest')
    # axs2[0].set_title("Original Image")
    #
    # axs2[1].imshow(centered_image, cmap=plt.cm.gray, interpolation='nearest')
    # axs2[1].set_title("centered Image")
    #plt.show()

hdf = h5py.File(filepath+'centered'+filename, 'w')
hdf.create_dataset('encoder', data=np.array(hf.get('encoder')))
hdf.create_dataset('ptychogram', data=NewPtychogram)
#hdf.create_dataset('background', data=np.array(hf.get('background')))  # Background images
hdf.create_dataset('zo', data=14.5e-3)
hdf.create_dataset('Nd', data=Ptycohgram[1].shape[0]*Ptycohgram[1].shape[1])  # number of the detector pixels
# hdf.create_dataset('dxd', np.array(hf.get('dxd')))
# hdf.create_dataset('wavelength', np.array(hf.get('wavelength')))
# hdf.create_dataset('entrancePupilDiameter', np.array(hf.get('entrancePupilDiameter')))

hdf.create_dataset('dxd', data=3.45e-6) #the size of the detector pixel in meter
hdf.create_dataset('wavelength', data=450e-9) #the wavelength of the
hdf.create_dataset('entrancePupilDiameter', data=0.5e-3) #entrancePupilDiameter, 1.587e-3
hdf.create_dataset('orientation', data=5)
