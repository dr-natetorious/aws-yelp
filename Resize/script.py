#!/usr/bin/python

from matplotlib import pyplot as plt
import numpy as np
import cv2

img = cv2.imread('./Resize/test.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)/255.0
dim = (64,64)
resized = cv2.resize(gray, dim, interpolation=cv2.INTER_AREA)
plt.imshow(resized[:,::-1])