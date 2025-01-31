import cv2
import mediapipe as mp
import numpy as np
import time
import math 
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam , hCam = 640 , 480


cap = cv2.VideoCapture(0)
cap.set(3 , wCam)
cap.set(4 , hCam)
pTime = 0


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volume.GetMute()
volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange() 
volume.SetMasterVolumeLevel(vol, None) # To set volume on your computer
minVol = volRange[0]
maxVol = volRange[1]
volBar = 0
vol  = 400
volPer = 0


mpHand = mp.solutions.hands
hands = mpHand.Hands()


mpDraw = mp.solutions.drawing_utils

while True:
    _ , img = cap.read()

    imgRGB = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    lmList = []

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img , handLms , mpHand.HAND_CONNECTIONS )

        for id , lm in enumerate(handLms.landmark):
            h , w , _ = img.shape
            cx , cy = int(lm.x * w) , int(lm.y * h)
            lmList.append([id , cx ,cy])

        if len(lmList) !=0 :
            
            x1 , y1 = lmList[4][1] , lmList[4][2]
            x2 , y2 = lmList[8][1] , lmList[8][2]

            cx , cy = (x1+x2)//2 , (y1+y2)//2

            cv2.circle(img , (x1 , y1) , 15 , (0 , 255 ,255) , cv2.FILLED )
            cv2.circle(img , (x2 , y2) , 15 , (0 , 255 ,255) , cv2.FILLED )
            cv2.line(img , (x1,y1) , (x2,y2) , (0 , 255 , 255) , 3 )
            cv2.circle(img , (cx , cy) , 15 , (0 , 255 ,255) , cv2.FILLED )

            length = math.hypot(x2-x1 , y2-y1)
            #print(length)

            #Hand Range 20-250
            #Volume Range -65 - 0

            vol = np.interp(length , [25,240] , [minVol , maxVol])
            volBar = np.interp(length , [25,240] , [400 , 150])
            volPer = np.interp(length , [50 ,300] , [0 ,100])
            print(vol)

            if length < 25:
                cv2.circle(img , (cx , cy) , 15 , (0 , 255 ,0) , cv2.FILLED )

    cv2.rectangle(img , (50 ,150) , (85,400) , (0 , 0 , 255) , 3)
    cv2.rectangle(img , (50 ,int(volBar)) , (85,400) , (0 , 0 , 255) , cv2.FILLED)
    cv2.putText(img , f'{int(volPer)} %' , (40, 450) , cv2.FONT_HERSHEY_PLAIN , 1 , (0,0,255) , 3)

    
    
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img , f'FPS: {int(fps)}' , (10 , 30) , cv2.FONT_HERSHEY_PLAIN , 2 , (255 , 0 , 0) , 2)

    cv2.imshow("Img",img)
    cv2.waitKey(1)






