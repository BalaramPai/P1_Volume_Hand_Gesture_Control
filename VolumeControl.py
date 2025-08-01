#Basic imports needed to Run the File.
import cv2
import numpy as np
import HTMFinalModule as htm   #Import HTMFinalModule created which has detection class.
import time
import mediapipe
import math             #For Hypotenuse.

################################################################

#AndreMiras/pycaw -- GitHub repository
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume

#################################################################

#AndreMiras/pycaw -- GitHub repository

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume = cast(interface,POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
#volRange = volume.GetVolumeRange()                #-65.25, 0.0

##################################################################

wcam,hcam = 640,480      #Parameters of window.
ptime,ctime = 0,0
vol = 0                 #Volume in scalar form variable.
volBar = 0              #For the volume bar.
volPercent = 0          #For the percentage of volume.

##################################################################

cap = cv2.VideoCapture(0)
#Setting dimensions of the window.
cap.set(3,wcam)
cap.set(4,hcam)

detector = htm.detection()      #Make a 'detector' object out of 'htm module' and 'detection' class in it.

##################################################################

while True:

    success, img = cap.read()
    img = cv2.flip(img,1)


    img = detector.find_my_hands(img)

    if detector.result_img.multi_hand_landmarks:
        num = len(detector.result_img.multi_hand_landmarks)

        lm = []

        for i in range(num):
            lm = detector.hand_position(img,handNo=i)
            if(len(lm)!=0):

                x1,y1 = lm[4][1],lm[4][2]           #Thumb Fingertips x and y coordinates.
                x2,y2 = lm[8][1],lm[8][2]           #Index Fingertips x and y coordinates.
                cx,cy = (x1+x2)//2,(y1+y2)//2       #Centre of the Thumb and Index finger.

                length = math.hypot(x2-x1,y2-y1)        #Length between Index and Thumb Finger.

                cv2.circle(img,(x1,y1),7,(255,0,255),cv2.FILLED) #Circle on Thumb Finger.
                cv2.circle(img, (x2, y2), 7, (255, 0, 255), cv2.FILLED) #Circle in Index Finger.
                cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED) #Circle in Between.
                cv2.line(img,(x1,y1),(x2,y2),(255,0,0),2)      #Line from Index to Thumb Finger.

                vol = np.interp(length,[30,190],[0.0,1.0])   #Convert the shortest and longest length to scalar.
                volBar = np.interp(length,[30,190],[400,150])   #Volume Bar 30-190 len to 400-150 pixels.
                volPercent = int(vol*100)                   #Convert the Scalar value into percentage and integer.
                volume.SetMasterVolumeLevelScalar(vol,None)

                cv2.rectangle(img,(50,150),(85,400),(255,0,0))   #Top left corner and Bottom Right corner
                cv2.rectangle(img,(50,int(volBar)),(85,400),(255,0,0),cv2.FILLED)   #To fill how much ever is volume.
                cv2.putText(img,f"{int(volPercent)}%",(40,450),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),2)

    #Fps Calculation.
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime

    cv2.putText(img,f'FPS:{int(fps)}',(10,70),2,cv2.FONT_HERSHEY_PLAIN,(255,255,255),2)

    cv2.imshow("MyImage",img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


