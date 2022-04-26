import cv2
import os
import hand
import math
import numpy
from pynput.keyboard import Key, Controller
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def distance(a,b):
    return int(math.sqrt((a[1]-b[1])**2+(a[2]-b[2])**2))

def gapngon(lmList):
    if len(lmList)!=0:
        if lmList[12][2] > lmList[9][2]:
            return True
        return False
    return False

def press(button, lmList):
    if len(lmList)!=0:
        check=False
        if gapngon(lmList)==True:
            if check==False:
                keyboard.press(button)
                keyboard.release(button)
                check=True
        else: 
            check=False

def change_mode(lmList, ButtonPressed, Mode):
    if len(lmList)!=0:
        if 0< lmList[8][2] <40 and 600< lmList[8][1] <640:
            if ButtonPressed==False:
                ButtonPressed=True
                Mode= not Mode
        else:
            ButtonPressed=False


#video source
cap=cv2.VideoCapture(0)
#keyboard controller
keyboard=Controller()
#volume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

#check da nhan nut chua
VMode=True
ButtonPressed=False

#vong lap chinh
while True:
    ret, frame=cap.read()

    detector=hand.handDetector(detectionCon=int(0.55))
    frame=detector.findHands(frame)
    lmList=detector.findPosition(frame, draw=False)
    #lat anh
    #frame= cv2.flip(frame,1)

    
    
    cv2.rectangle(frame,(600,0), (640,40),(255,0,0),-1)
    change_mode(lmList, ButtonPressed,VMode)
    if VMode==False: 
        cv2.rectangle(frame,(20,0), (180,150),(0,0,0),3)
        cv2.rectangle(frame,(220,0), (380,150),(0,0,0),3)
        cv2.rectangle(frame,(420,0), (580,150),(0,0,0),3)
        #xet vi tri tay
        if len(lmList)!=0:
            if 20<lmList[12][1]<180:
                press(Key.left)
            elif 220<lmList[12][1]<380:
                press(Key.space)
            elif 420<lmList[12][1]<580:
                press(Key.right)
    else:
        cv2.rectangle(frame,(600,150),(640,400),(255,255,0),-1)

    frame=cv2.resize(frame,(0,0),fx=1.3,fy=1.3)
    cv2.imshow('pmc',frame)
    if cv2.waitKey(1)==ord('g'):
        break

cap.release()
cv2.destroyAllWindows()



# hệ quy chiếu khi lật ảnh
# hàm gapngon