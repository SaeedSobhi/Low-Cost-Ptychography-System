from pymba import Vimba
import numpy as np
import matplotlib.pyplot as plt

with Vimba() as vimba:
    camera = vimba.camera(0)
    print(camera)
    camera.open()
    camera.arm('SingleFrame')
    exposure_time = camera.ExposureTime

    # get a copy of the frame data
    frame = camera.acquire_frame()
    image1 = frame.buffer_data_numpy()

#snap a square around the center
MinShape = np.min(image1.shape)
MaxShape = np.max(image1.shape)
if MinShape == image1.shape[0]:
    image = image1[:, (MaxShape-MinShape)//2:(MaxShape+MinShape)//2]
    SquareCaptionOrder = 1
elif MinShape == image1.shape[1]:
    image = image1[(MaxShape - MinShape)//2:(MaxShape + MinShape)//2, :]
    SquareCaptionOrder = 2
else:
    image = image1

binned_image = np.zeros([image.shape[0]//3, image.shape[1]//3])

print(binned_image.shape)
b = 0
for j in range(1, image.shape[0] - 3, 3):
    a = 0
    for i in range(1, image.shape[1] - 3, 3):
        binned_image[b, a] = np.average(image[j-1:j+1, i-1:i+1])
        a = a + 1
    b = b + 1

fig1, ax = plt.subplots(1, 2, figsize=(9, 9))
ax[0].imshow(binned_image, cmap=plt.gray())
ax[0].set_title('Binned Image')
ax[1].imshow(image, cmap=plt.gray())
ax[1].set_title('Original Image')

plt.show()
