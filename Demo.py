import cv2
import os
import hand
import math
import numpy
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def distance(a,b):
    return int(math.sqrt((a[1]-b[1])**2+(a[2]-b[2])**2))

cap=cv2.VideoCapture(0)

#hand detector   
detector=hand.handDetector(detectionCon=int(0.55))
finger=[8,12,16,20]

#volume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

while True:
    ret, frame=cap.read()
    frame=detector.findHands(frame)
    lmList=detector.findPosition(frame, draw=False)
    
    cv2.rectangle(frame,(0,100),(100,300),(255,255,0),-1)
    
    if len(lmList)!=0:
        check=True
        for i in range (1,4):
            if lmList[finger[i]][2] < lmList[finger[i]-2][2]:
                check=False
        if check==True:
            a=distance(lmList[8],lmList[4])
            cv2.circle(frame,(lmList[8][1],lmList[8][2]),10,(0,0,0),-1)
            cv2.circle(frame,(lmList[4][1],lmList[4][2]),10,(0,0,0),-1)
            cv2.line(frame,(lmList[8][1],lmList[8][2]),(lmList[4][1],lmList[4][2]),(0,0,0),2)
            vol=numpy.interp(a,(20,260),(-62.25,0))
            volume.SetMasterVolumeLevel(vol, None)
    frame= cv2.flip(frame,1)
    cv2.imshow('pmc',frame)
    if cv2.waitKey(1)==ord('g'):
        break
cap.release()
cv2.destroyAllWindows()
