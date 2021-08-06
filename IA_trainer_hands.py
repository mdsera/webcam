import cv2
import numpy as np
import time
import body_detection as pm
import pyttsx3
import hand_detection_modele as hdm
import os
from PIL import Image

engine = pyttsx3.init()
voice = engine.getProperty('voices')[0]  # English voice
engine.setProperty('rate', 125)
engine.setProperty('voice', voice.id)
# engine.say('Welcome to Marco s app')
# engine.runAndWait

folderPath = "/Users/marcosera/desktop/python_projects/camera_avec/cam_detection/project_personal/images"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
dim = (250, 250)
for imPath in myList:
    if not imPath.endswith('DS_Store'):
        image = Image.open(f'{folderPath}/{imPath}').convert('RGB')
        image = image.resize(dim, Image.ANTIALIAS)
        overlayList.append(image)
        image = image.convert('1')
        image = image.convert('RGB')
        overlayList.append(image)

cap = cv2.VideoCapture(0)

detector = pm.poseDetector()
hand_detector = hdm.handDetector(detectionCon=0.75, maxHands=1)
RA_count = 0
LA_count = -0.5
Leg_count = 0
dir = 0
ldir = 0
legdir = 0
exercice_title = 'Select Exercice'

pTime = 0
while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))
    img_hand = hand_detector.findHands(img, draw=False)
    hand_lmList = hand_detector.findPosition(img_hand, draw=False)
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    # fingers = hand_detector.fingersUp()
    # print(fingers)

    if len(hand_lmList) != 0:
        x1, y1 = hand_lmList[8][1:]  # index finger
        x2, y2 = hand_lmList[12][1:]  # middle finger
        # x3, y3 = hand_lmList[16][1:]  # ring finger
        # x4, y4 = hand_lmList[20][1:]  # pinky finger
        # x5, y5 = hand_lmList[4][1:]  # thumb
        print(hand_lmList[8][2], hand_lmList[6][2])
        if (hand_lmList[8][2] < hand_lmList[6][2]) and (hand_lmList[12][2] < hand_lmList[10][2]) and (hand_lmList[16][2] > hand_lmList[14][2]) and (hand_lmList[20][2] > hand_lmList[18][2]) and (hand_lmList[4][2] > hand_lmList[5][2]):
            # cv2.rectangle(img_hand, (x1, y1 - 25), (x2, y2 + 25),
            #               (177, 177, 0), cv2.FILLED)
            cv2.circle(img_hand, (int((x1+x2)/2), int((y1+y2)/2)),
                       10, (0, 255, 0), cv2.FILLED)
            img[10:260, 50:300] = overlayList[1]
            img[10:260, 600:850] = overlayList[3]
            if (y1+y2)/2 < 260:
                if 50 < (x1+x2)/2 < 300:
                    img[10:260, 50:300] = overlayList[0]
                    exercice_title = 'Arm weight lifting'
                elif 600 < (x1+x2)/2 < 850:
                    img[10:260, 600:850] = overlayList[2]
                    exercice_title = 'Squats'

    if len(lmList) != 0:

        # Right Arm
        right_angle = detector.findAngle(img, 12, 14, 16)
        # Left Arm
        left_angle = detector.findAngle(img, 11, 13, 15, True)
        # Back
        back_angle = detector.findAngle(img, 12, 24, 26, True)
        back1_angle = detector.findAngle(img, 11, 23, 25, True)
        # legs
        lright_angle = detector.findAngle(img, 24, 26, 28, True)
        lleft_angle = detector.findAngle(img, 23, 25, 27, True)

        rleg_per = np.interp(lright_angle, (85, 180), (0, 100))
        lleg_per = np.interp(lleft_angle, (85, 180), (0, 100))

        back_per = np.interp(right_angle, (210, 310), (0, 100))
        back_per = np.interp(right_angle, (210, 310), (0, 100))

        left_per = np.interp(left_angle, (45, 170), (0, 100))
        # left_bar = np.interp(left_angle, (220, 310), (650, 100))

        per = np.interp(right_angle, (210, 310), (0, 100))
        # bar = np.interp(right_angle, (220, 310), (650, 100))
        # print(angle, per)

        # Check for the dumbbell curls
        # color = (255, 0, 255)
        if per == 100:
            # color = (0, 255, 0)
            if dir == 0:
                RA_count += 0.5
                dir = 1
        if per == 0:
            # color = (0, 0, 255)
            if dir == 1:
                RA_count += 0.5
                dir = 0

        if left_per == 100:
            if ldir == 0:
                LA_count += 0.5
                ldir = 1
        if left_per == 0:
            if ldir == 1:
                LA_count += 0.5
                ldir = 0

        if lleg_per == 100 or rleg_per == 100:
            if legdir == 0:
                Leg_count += 0.5
                legdir = 1
        if lleg_per == 0 or rleg_per == 0:
            if legdir == 1:
                Leg_count += 0.5
                legdir = 0

        # Draw Bar
        # cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        # cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        # cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
        #             color, 4)

        # Draw Curl Count
        # Right arm
        cv2.rectangle(img, (0, 660), (130, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, 'RArm', (35, 650), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 255, 255), 2)
        cv2.putText(img, str(int(RA_count)), (20, 710), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 2,
                    (255, 0, 0), 2)

        # Left arm
        cv2.rectangle(img, (0, 560), (130, 620), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, 'LArm', (35, 550), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 255, 255), 2)
        cv2.putText(img, str(int(LA_count)), (20, 610), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 2,
                    (255, 0, 0), 2)

        # Legs
        cv2.rectangle(img, (0, 460), (130, 520), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, 'Legs', (35, 450), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 255, 255), 2)
        cv2.putText(img, str(int(Leg_count)), (20, 510), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 2,
                    (255, 0, 0), 2)

    cv2.putText(img, str(exercice_title), (420, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3,
                (0, 0, 255), 2)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_PLAIN, 2,
                (0, 0, 0), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        engine.say('Have a nice day!')
        engine.runAndWait()
        break
