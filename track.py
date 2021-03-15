# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 13:51:18 2021

@author: coxbox
"""
import cv2 
import numpy as np
from skimage.filters import gaussian
from skimage.measure import label, regionprops
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu
from skimage.morphology import closing, square, erosion
from skimage.io import imsave

median_im = np.array(median_im)
median_im = np.median(median_im,0)
cap = cv2.VideoCapture(r'C:\Users\Conor\Documents\GitHub\Slice-and-dist-count\Video 2006.wmv')
base_mask = np.zeros(np.shape(img))
#masks ar defined by top left then bottom rigth

mask1 = cv2.rectangle(base_mask, (target_points[0][0],target_points[0][1]),(target_points[1][0],target_points[1][1]), (1,1,1), -1)
base_mask = np.zeros(np.shape(img))
mask2 = cv2.rectangle(base_mask, (target_points[2][0],target_points[2][1]),(target_points[3][0],target_points[3][1]), (1,1,1), -1)
base_mask = np.zeros(np.shape(img))
mask3 = cv2.rectangle(base_mask, (target_points[4][0],target_points[4][1]),(target_points[5][0],target_points[5][1]), (1,1,1), -1)
base_mask = np.zeros(np.shape(img))
mask4 = cv2.rectangle(base_mask, (target_points[6][0],target_points[6][1]),(target_points[7][0],target_points[7][1]), (1,1,1), -1)
masks = [mask1,mask2,mask3,mask4]

i=0
output = []
while(cap.isOpened()):
    ret,frame = cap.read()

    if ret == False:
        break
    i+=1
    if i%100 ==0:
        print(i/15)
    if i%2==0:
        continue
    img = np.mean(frame,2)
    img = gaussian(img,sigma=3)
    img = np.abs(img-median_im)
    inner_output= []
    for mnn,mask in enumerate(masks):
        temp_frame = img*mask
        thresh = threshold_otsu(temp_frame)
        bw = (temp_frame>thresh)
        label_image = label(bw)
        props = regionprops(label_image)
        areas = [x.area for x in props]
        big_obj = props[np.argmax(areas)]
        inner_output= [big_obj.centroid[1],big_obj.centroid[0]]
    output.append(inner_output)