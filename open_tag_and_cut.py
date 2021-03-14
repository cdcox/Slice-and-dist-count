# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 13:44:25 2021

@author: Conor
"""

import cv2 

cap = cv2.VideoCapture(r'C:\Users\Conor\Documents\GitHub\Slice-and-dist-count\Video 2006.wmv')
#directory = r'C:\Users\Conor\Desktop\TRNDeepnetWorkingdir\AL_trn files'
FPS =  cap.get(cv2.CAP_PROP_FPS)

def draw_circle(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img,(x,y),5,(255,0,0),-1)
        zz.append([x,y])
        
        
#loop to write some dots
zz=[]
i=0

while(cap.isOpened()):
    i+=1
    ret,frame = cap.read()
    if i ==200:
        img = frame
        cv2.namedWindow('image')
        cv2.setMouseCallback('image',draw_circle)
        while(1):
            cv2.imshow('image',img)
            if cv2.waitKey(20) & 0xFF == 27:
                break
        cv2.destroyAllWindows()
        break
    
#cap = cv2.VideoCapture(r'C:\Users\Conor\Desktop\TRNDeepnetWorkingdir\AL_trn files\Video 1099.wmv')
#FPS =  cap.get(cv2.CAP_PROP_FPS)