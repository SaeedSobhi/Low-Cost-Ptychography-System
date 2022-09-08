import cv2
import numpy as np
import h5py
import imageio
import pandas as pd
import matplotlib.pyplot as plt
import io
from PIL import Image

hf = h5py.File('hdf5Data/05_08_2022_12_25_19.hdf5', 'r')

Ptycohgram = np.array(hf.get('ptychogram'))

plt.imshow(Ptycohgram[2], cmap=plt.gray())
plt.show()
fgfggg
#hf = h5py.File('D:/daniel/Datasets/preprocessed/31012022_div_1.hdf5', 'r')

# print(hf.keys())
# # for x in hf.get('dxd'):
# #     print(x)
# # print(hf.get('dxd'))
# #lklkjj
# for key in hf.keys():
#     print(hf.get(key))
    #print(hf.get(key)[0])

#print(hf.get('encoder')[1])
# Nd: number of  detector pixels, single
# background
# zo: object camera distance, single
#Data1 = np.loadtxt("UC2_PtychCoords.txt", dtype=float)
Data1 = np.loadtxt("0.1Spiral200.txt", dtype=float)

# data = pd.DataFrame(Data1)
# # storing into the excel file
# data.to_excel("Spiral200.xlsx")
#Data = Data1.astype(np. float)

radii = np.hypot(Data1[:, 0], Data1[:, 1])
Data1 = Data1[radii < 0.9] #Get the closest 50 points to the center  193
radii_sorted = np.sort(radii)
#print(radii_sorted[100])
print(Data1.shape)
#circle1 = plt.Circle((0, 0), 0.5, color='blue', fill=False)

plt.scatter(*zip(*Data1), color='red')
cnt = 0
'''
for D in Data1:
    #if cnt % 3 == 0:
    #if 60 < cnt < 63:
    circle1 = plt.Circle((D[0], D[1]), 0.5, color='blue', fill=False)
    plt.gca().add_patch(circle1)
    # elif 76 < cnt < 80:
    #     circle1 = plt.Circle((D[0], D[1]), 0.5, color='black', fill=True)
    #     plt.gca().add_patch(circle1)

    # elif cnt%3 == 0:
    #     circle1 = plt.Circle((D[0], D[1]), 0.5, color='black', fill=False)
    # elif cnt%2 == 0:
    #     circle1 = plt.Circle((D[0], D[1]), 0.5, color='red', fill=False)
    # else:
    #     circle1 = plt.Circle((D[0], D[1]), 0.5, color='purple', fill=False)
    cnt = cnt + 2
'''
plt.set_aspect(1)

plt.gca().set_aspect('equal')
plt.title('The scanning grid while showing the expected overlap')
plt.xlabel('X_position (mm)')
plt.ylabel('Y_position (mm)')
plt.show()
gffg

Data = Data1.astype(np. float)
print(type(Data1[0, 0]))
#radii = np.hypot(Data[:, 0], Data[:, 1])
#Data = Data[radii < 193] #Get the closest 50 points to the center  193

Data[:, 0] = (Data[:, 0]*3.89e-6)/1.45
Data[:, 1] = (Data[:, 1]*3.89e-6)/1.45

measured_Data = hf.get('encoder')
plt.scatter(*zip(*Data), color='red')
plt.scatter(*zip(*measured_Data), color='blue', label='measured-positions')
plt.title("Measured Coordinates (red) Vs. Given Coordinates (Blue)")

plt.show()
#Ptycohgram = np.array(hf.get('ptychogram'))
#background = np.array(hf.get('background'))
#BinFactor = np.array(hf.get("binningFactor"))
#print(np.average(background[0, :, :]))
#GifTemplate = []
#GifTemplate.append(background[0, :, :])
#print(BinFactor)

#imageio.mimsave('background.tif', background)
#rreerr
mxdata1 = np.array(measured_Data)

mxdata2 = mxdata1 * 1000
mxdata = mxdata2.tolist()

#imageio.mimsave('background.gif', Ptycohgram, duration=0.3)

#np.savez('positions.npz', actual_positions=mxdata)


# for i, position in enumerate(measured_Data):
#     #print(position)
#     plt.clf()
#     plt.grid()
#     plt.scatter(*zip(*measured_Data))
#     plt.plot(position[1], position[0], marker="o", markersize=5, markeredgecolor="red", markerfacecolor="green")
#     #plt.title('Sample position in micro meter')
#     img_buf = io.BytesIO()
#     plt.savefig(img_buf, format='png')
#     im = Image.open(img_buf)
#     GifTemplate.append(im.copy())
#     GifTemplate.append(Ptycohgram[i, :, :])

#imageio.mimsave('050422_50points+diffractionPattern.gif', GifTemplate, duration=1)

'''
for img in background:
    print(np.average(img))
print(background.shape)
'''
Data = np.loadtxt("UC2_PtychCoords.txt", dtype=float)
radii = np.hypot(Data[:, 0], Data[:, 1])
Data = Data[radii < 193] #Get the closest 50 points to the center

#L = []
#L1 = sorted(L)
#print(L1[50])
# forming dataframe
data = pd.DataFrame(measured_Data)
# storing into the excel file
data.to_excel("measured_Data.xlsx")

cnt = 0

#print(Data)

#measured_Data.pop(16)
#measured_Data = measured_Data

#plt.scatter(*zip(*measured_Data), color='blue')
#plt.scatter(*zip(*Data), color='red')
#plt.plot(Data[:, 0], Data2[:, 0])

fig1, ax = plt.subplots(1, 2, figsize=(9, 9))
ax[0].scatter(*zip(*measured_Data), color='blue')
ax[0].set_title('measured data')

ax[1].scatter(*zip(*Data), color='red')
ax[1].set_title('from text file')
'''
plt.title('Positions of the recorded diffraction patterns')
plt.xlabel('Y_position, micro meter')
plt.ylabel('X_position, micro meter')
'''

plt.show()

