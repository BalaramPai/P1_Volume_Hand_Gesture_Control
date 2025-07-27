import cv2                         #Import Cv Module(Interpreter 3.7 - 3.10).
import time
import mediapipe as mp             #Import Mediapipe Framework by Google.

########################################################

#Create a detection class with important methods needed.
class detection():
    def __init__(self,mode=False,maxHands=2,model_complexity=1,detectionCon=0.5,trackCon=0.5):  #Initialise Variables.
        self.mode = mode
        self.maxHands = maxHands
        self.model_complexity = model_complexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.module = mp.solutions.hands          #So in MediaPipe there is a Module called 'hands'.
        #Create an object out of 'Hands' class in 'hands' module.
        self.obj = self.module.Hands(self.mode,self.maxHands,self.model_complexity,self.detectionCon,self.trackCon)
        self.drawer = mp.solutions.drawing_utils  #Drawing Utilities in Mediapipe as drawing_utils module.


    #This function is to recognise my Hands and give it the 21 Landmarks as an image.
    def find_my_hands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)       #Converting the BGR image to RGB image.
        self.result_img = self.obj.process(imgRGB)          #This is the converted image which I can use.

        if self.result_img.multi_hand_landmarks:            #If any hand is recognised or can be seen.
            # As the multi_hand_landmarks returns nested list we access each hand using a for loop.
            for hand in self.result_img.multi_hand_landmarks:
                if draw:
                    #Using the drawer object we use draw_landmarks where HAND_CONNECTIONS is a constant in hands Module.
                    self.drawer.draw_landmarks(img,hand,self.module.HAND_CONNECTIONS)
        return img   #Return the image with landmarks.


    #This function is to map the locations or co-ordinates of each landmark into a list as pixel co-ordinates.
    def hand_position(self,img,handNo=0,draw=True):
        lmlist = []

        if self.result_img.multi_hand_landmarks:           #If a hand is detected.
            myhand = self.result_img.multi_hand_landmarks[handNo]   #Each hand based on the Hand number.

            for id, lm in enumerate(myhand.landmark):      #We take landmark of each hand and then convert it to pixels.
                h,w,c = img.shape                          #Extract the height and width and channel(RGB).

                cx,cy = int(lm.x*w),int(lm.y*h)            #Convert from relative position to screen to PIXELS,
                lmlist.append([id,cx,cy])                  #Add it to the list created.
        return lmlist                                      #Return the formed list of landmarks.

########################################################

#Main function is used for self Testing purpose.
def main():

    #Variables needed are declared for current and pastime in FPS calculations.
    ctime = 0
    ptime = 0

    #Create an object called detector out of the detection class for using methods.
    detector = detection()

    #Capture the Video from the default in-built camera(0) and external can be (1).
    cap = cv2.VideoCapture(0)

    #To capture every frame.
    while True:
        #Capture the frames into img variable.
        success, img = cap.read()
        img = cv2.flip(img, 1)   #Make the video mirror image.
        img = detector.find_my_hands(img)   #Detect the hands and give em landmarks and return to img variable.

        #fps calculation.
        ctime = time.time()
        fps = 1/(ctime-ptime)
        ptime = ctime

        #If a hand is detected.
        if detector.result_img.multi_hand_landmarks:
            num = len(detector.result_img.multi_hand_landmarks)   #Count number of hands detected.

            lm=[]

            for i in range(num):        #For each hand.
                lm = detector.hand_position(img,i)     #Obtain position of each landmark of each hand.
                if len(lm)>0:
                    print(lm[8])                       #Print the position of the landmark-8 , tip of index-finger.

        #Show the Frames Per Second as Text.
        cv2.putText(img,f'FPS:{int(fps)}',(10,70),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
        cv2.imshow("Image", img)    #Display the Video-Capture in a new window called Image.
        cv2.waitKey(1)                      #A delay given to process frames.


if __name__ == '__main__':
    main()                              #Self Run.



