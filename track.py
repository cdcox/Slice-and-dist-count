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
import os
import imageio
import csv
import xlwt 

directory = r'C:\Users\coxbox\Documents\GitHub\Slice-and-dist-count\work_dir'
file_list = os.listdir(directory)
temp_points_all = []

with open(os.path.join(directory,'points.txt'),'r') as csv_file:
    for line in csv_file:
        temp_points_all.append(line[:-2])

target_points_all =[]
internal = []
for temp_points in  temp_points_all:
    temp_points=temp_points.split(',')
    if '.wmv' in temp_points[0]:
        target_points_all.append(internal)
        internal = [temp_points[0]]
    else:
        internal.append([int(temp_points[0][1:]),int(temp_points[1])])
out_v=[]    
for v_file in file_list:
    if not('.wmv' in v_file[-5:]):
        continue
    for knn,key_target in enumerate(internal):
        if v_file in key_target:
            break
    print(v_file)
    target_points= internal[knn+1:knn+9]
    out_v.append(v_file)
        
    median_im = imageio.imread(os.path.join(directory,v_file+'.png'))
    cap = cv2.VideoCapture(os.path.join(directory,v_file))
    base_mask = np.zeros(np.shape(median_im))
    #masks ar defined by top left then bottom rigth
    
    mask1 = cv2.rectangle(base_mask, (target_points[0][0],target_points[0][1]),(target_points[1][0],target_points[1][1]), (1,1,1), -1)
    base_mask = np.zeros(np.shape(median_im))
    mask2 = cv2.rectangle(base_mask, (target_points[2][0],target_points[2][1]),(target_points[3][0],target_points[3][1]), (1,1,1), -1)
    base_mask = np.zeros(np.shape(median_im))
    mask3 = cv2.rectangle(base_mask, (target_points[4][0],target_points[4][1]),(target_points[5][0],target_points[5][1]), (1,1,1), -1)
    base_mask = np.zeros(np.shape(median_im))
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
            inner_output.append([big_obj.centroid[1],big_obj.centroid[0]])
        output.append(inner_output)

wb = xlwt.Workbook() 
sheet1 = wb.add_sheet('Outputs')

for vnn,v_file in enumerate(out_v):
    for i in range(4):
        sheet1.write(0,vnn*8+i*2,v_file+'x')
        sheet1.write(0,vnn*8+i*2+1,v_file+'y')
        for j in range(len(output)):
            xy = output[j][vnn*4+i]
            sheet1.write(j+1,vnn*8+i*2,xy[0])
            sheet1.write(j+1,vnn*8+i*2+1,xy[1])
wb.save(os.path.join(directory,'track_plot.xls'))
            