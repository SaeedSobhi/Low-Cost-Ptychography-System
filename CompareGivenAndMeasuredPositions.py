import numpy as np
import h5py
import imageio
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker

hf = h5py.File('hdf5Data/03_08_2022_17_24_12.hdf5', 'r')

Data1 = np.loadtxt("0.1Spiral200.txt", dtype=float)
radii = np.hypot(Data1[:, 0], Data1[:, 1])
Data1 = Data1[radii < 1.1]
#Data1 = Data1.astype(np. float)
Data1 = Data1 * 10e-4

measured_Data = hf.get('encoder')
measured_Data = measured_Data.astype(np. float)
#measured_Data = measured_Data * 10e4
plt.gca().set_aspect('equal')
plt.gca().get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x*1000), ',')))
plt.gca().get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x*1000), ',')))
plt.xlabel('X_position (mm)')
plt.ylabel('Y_position (mm)')
plt.scatter(*zip(*Data1), color='red', label='given-positions', marker='+')
plt.scatter(*zip(*measured_Data), color='blue', label='measured-positions', marker='x')
plt.title("Measured Coordinates (red) Vs. Given Coordinates (Blue)")

# Fontsize = 20
# fig1, ax = plt.subplots(1, 2, figsize=(16, 16))
# ax[0].set_box_aspect(1)
# ax[0].scatter(*zip(*measured_Data), color='red')
# ax[0].set_title('Measured Coordinates', fontsize=Fontsize)
# ax[0].set_xlabel('X_position (mm)', fontsize=Fontsize)
# ax[0].set_ylabel('Y_position (mm)', fontsize=Fontsize)
# ax[0].yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x*1000), ',')))
# ax[0].xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x*1000), ',')))
#
# ax[1].set_box_aspect(1)
# ax[1].scatter(*zip(*Data1), color='blue')
# ax[1].set(aspect='equal')
# ax[1].set_title('Given Coordinates', fontsize=Fontsize)
# ax[1].set_xlabel('X_position (mm)', fontsize=Fontsize)
# ax[1].set_ylabel('Y_position (mm)', fontsize=Fontsize)
# ax[1].yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x*1000), ',')))
# ax[1].xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x*1000), ',')))
#


plt.show()

