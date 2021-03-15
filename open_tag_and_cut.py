# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 13:44:25 2021

@author: Conor
"""

import cv2 
import numpy as np
from skimage.filters import gaussian
from skimage.measure import label, regionprops
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu
from skimage.morphology import closing, square, erosion
import os
from skimage.io import imsave
import csv


directory = r'C:\Users\coxbox\Documents\GitHub\Slice-and-dist-count\work_dir'
file_list = os.listdir(directory)
target_points_all = []
for v_file in file_list:
    if not('.wmv' in v_file):
        continue
    cap = cv2.VideoCapture(os.path.join(directory,v_file))
    #directory = r'C:\Users\Conor\Desktop\TRNDeepnetWorkingdir\AL_trn files'
    FPS =  cap.get(cv2.CAP_PROP_FPS)
    
    def draw_circle(event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(img,(x,y),5,(255,0,0),-1)
            target_points.append([x,y])
            
            
    #loop to write some dots
    target_points=[v_file]
    i=0
    median_im = []
    while(cap.isOpened()):
        i+=1
        ret,frame = cap.read()
        if ret == False:
            break
        if i ==200:
            img = frame
            cv2.namedWindow('image')
            cv2.setMouseCallback('image',draw_circle)
            while(1):
                cv2.imshow('image',img)
                if cv2.waitKey(20) & 0xFF == 27:
                    break
            cv2.destroyAllWindows()
        if i%25==0:
            img= np.mean(frame,2)
            median_im.append(gaussian(img,sigma=3))
        
        if i ==1500:
            break
    median_im = np.array(median_im)
    median_im = np.median(median_im,0)
    imsave(os.path.join(directory,v_file,'.png'),median_im)
    
    
    
    
    
    
