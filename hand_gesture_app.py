import pmc_hand
import cv2
import math
import numpy
from pynput.keyboard import Key, Controller
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


def x_distance(a,b):
    return int(abs(a-b))


def in_volumebar(lmList):
    if len(lmList)!=0:
        if lmList[8][2] < 60:
            return True
        return False
    return False

def grab_hand(lmList):
    if len(lmList)!=0:
        for i in range(2,6):
            if lmList[i*4][2]< lmList[i*4-2][2]:
                return False
        return True
    return False

def left_hand(lmList):
    if len(lmList)!=0:
        if lmList[17][1] > lmList[4][1]:
            return True
        return False
    return False

def press_key(button):
    keyboard.press(button)
    keyboard.release(button)

#video source
cap=cv2.VideoCapture(0)
#keyboard controller
keyboard=Controller()
#volume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

#hand detector

detector=pmc_hand.handDetector(detectionCon=0.5)
switch=[False,False]

#vong lap chinh
while True:
    ret, frame=cap.read()

    frame=detector.handsFinder(frame)
    lmList=detector.positionFinder(frame, draw=False)
    if len(lmList)!=0:
        if grab_hand(lmList)==True and left_hand(lmList)==True and lmList[4][2]<lmList[2][2]:
            if switch[0]==False:
                press_key(Key.left)
                switch[0]=True
        else: switch[0]=False
    
        if grab_hand(lmList)==True and left_hand(lmList)==False and lmList[4][2]<lmList[2][2]:
            if switch[1]==False:
                press_key(Key.right)
                switch[1]=True
        else: switch[1]=False

        if in_volumebar(lmList)==True:
            vol=numpy.interp(x_distance(lmList[8][1],50),(0,540),(-65.25,0.0))
            volume.SetMasterVolumeLevel(vol, None)
    cv2.imshow("alo",frame)
    if cv2.waitKey(1)==ord('g'):
        break

cap.release()
cv2.destroyAllWindows()
