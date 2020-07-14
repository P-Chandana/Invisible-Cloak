'''import Libraries'''
import numpy as np
import cv2
import time

cap=cv2.VideoCapture(0)
#initially the camera output is dark , it improves with the time

time.sleep(2)

''' delay execution for a given number of seconds '''
#intialize a variable where we will be capturing the background which is displayed when cloak is worn

background = 0


for i in range(30):
    ret,background=cap.read()
    
while (cap.isOpened()):
    ret,image=cap.read()
    
    if not ret: #after closing the video camera , it will return false 
        break
        
    hsv_img=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    
    #HSV values
    lower_red=np.array([0,120,70])
    upper_red=np.array([10,255,255])
    #seperating the cloak part 
    mask1=cv2.inRange(hsv_img,lower_red,upper_red)
    
    lower_red=np.array([170,120,70])
    upper_red=np.array([180,255,255])
    mask2=cv2.inRange(hsv_img,lower_red,upper_red)
    
    ''' if there i any shade of red in range of 0-10 or in range of 170-180 it will be added to mask1'''
    
    mask1=mask1+mask2 # '+' indicates OR operation
    
    mask1=cv2.morphologyEx(mask1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8),iterations=2) #noise removal
    mask1=cv2.morphologyEx(mask1,cv2.MORPH_DILATE,np.ones((3,3),np.uint8),iterations=2) #smoothening
    
    mask2=cv2.bitwise_not(mask1) #everything except the cloak
    
    result1=cv2.bitwise_and(background,background,mask=mask1) #used for the segmentation of the color
    result2=cv2.bitwise_and(image,image,mask=mask2) #used to substituite the cloak part
    
    result=cv2.addWeighted(result1,1,result2,1,0)
    
    cv2.imshow('output',result)
    
    cv2.waitKey(1)   
cap.release()
cv2.destroyAllWindows()
    
   