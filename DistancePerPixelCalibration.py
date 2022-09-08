import urllib.request
import urllib
import cv2
import numpy as np
import matplotlib.pyplot as plt
import imutils
from imutils import perspective
from imutils import contours

url = 'http://192.168.137.61/cam-hi.jpg'

imgResp = urllib.request.urlopen(url)
imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
img = cv2.imdecode(imgNp, -1)
#cv2.imwrite("capture2.jpg", img)

#img = cv2.imread("capture1.jpg")
x, y, t = img.shape

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)
#thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)[1]

#gray2 = cv2.medianBlur(gray[x//4:3*x//4, y//4:3*y//4], 9)
scale = 1
delta = 0
ddepth = cv2.CV_16S

# Scharr or Sobel
#grad_x = cv2.Scharr(gray, ddepth, 1, 0)
grad_x = cv2.Sobel(gray, cv2.CV_16S, 1, 0, ksize=5, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
#grad_y = cv2.Scharr(gray, ddepth, 0, 1)
grad_y = cv2.Sobel(gray, cv2.CV_16S, 0, 1, ksize=5, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)

edged1 = np.abs(grad_x)#+grad_y)
edged2 = np.abs(grad_y)#+grad_y)

max_index_col = np.argmax(edged1, axis=0)
max_index_row = np.argmax(edged2, axis=1)
print(edged1.shape)
print(max_index_col.shape, max_index_col)
print(max_index_row.shape, max_index_row)

plt.imshow(gray, cmap=plt.gray(), interpolation='nearest')
plt.show()

fig, axs = plt.subplots(2, 3, figsize=(16, 9))

axs[0, 0].imshow(gray, cmap=plt.gray(), interpolation='nearest')
axs[0, 0].set_title("gray Image")

axs[0, 1].imshow(edged2, cmap=plt.gray(), interpolation='nearest')
axs[0, 1].set_title('after applying y-Sobel filter')

axs[0, 2].imshow(edged1, cmap=plt.gray(), interpolation='nearest')
axs[0, 2].set_title('after applying x-Sobel filter')

#axs[1, 0].plot(np.histogram(max_index_col)[2], np.histogram(max_index_col)[0])
#axs[1, 0].set_title("gray Image")

axs[1, 1].plot(max_index_col)
axs[1, 1].set_title('max_index_col')

axs[1, 2].plot(max_index_row)
axs[1, 2].set_title('max_index_row')

plt.show()

hist, bins = np.histogram(max_index_col)
plt.hist(max_index_col, bins)
plt.title("histogram")
plt.show()


'''
for i in range(0, edged1.shape[0]):
    for j in range(0, edged1.shape[1]):
'''


edged = edged1/np.max(edged1)

#edged = cv2.erode(edged, None, iterations=2)
#edged = cv2.dilate(edged, None, iterations=2)

'''
# find contours in the edge map
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
# sort the contours from left-to-right and initialize the
# 'pixels per metric' calibration variable
(cnts, _) = contours.sort_contours(cnts)
pixelsPerMetric = None
'''

'''
#histogram
histr = cv2.calcHist([edged], [0], None, [256], [0, 1])
plt.plot(histr)
plt.show()
'''

#Image normalization
#edged = edged/np.max(edged)
'''
dst = cv2.cornerHarris(gray, 2, 9, 0.04)
dst = cv2.dilate(dst, None)

dst = dst/np.max(dst)

#dst[dst < 0.50] = 0
#plt.imshow(edged, cmap=plt.gray(), interpolation='nearest')

#plt.imshow(dst, cmap=plt.gray(), interpolation='nearest')
img[dst > 0.01*dst.max()] = [0, 0, 255]

plt.imshow(img[x//4:3*x//4,y//4:3*y//4], cmap=plt.gray(), interpolation='nearest')
#plt.imshow(1-dst, cmap=plt.gray(), interpolation='nearest')

plt.show()
'''