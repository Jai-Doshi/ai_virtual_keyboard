import cv2      # pip intsall opencv-python
from cvzone.HandTrackingModule import HandDetector      # pip install mediapipe==0.8.7
import numpy as np      # pip install numpy
import cvzone       # pip install cvzone==1.4.1
from pynput.keyboard import Controller      # pip install pynput
from playsound import playsound     # pip install playsound
from time import sleep

# for webcam (Live Video)
cap = cv2.VideoCapture(0)

# Screen Resolution
cap.set(3, 1280)
cap.set(4, 720)

# Detecting the hands
detector = HandDetector(detectionCon=0.8)

# List of Keys
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

# Output Text
finalText = ""

# Keyboard key pressed
keyboard = Controller() 

# Drawing and styling the keyboard
def drawAll(img, buttonList):
    imgNew = np.zeros_like(img, np.uint8)
    for button in buttonList:
        x, y = button.pos
        cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                          20, rt=0)
        cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]),
                      (255, 0, 255), cv2.FILLED)
        cv2.putText(imgNew, button.text, (x + 40, y + 60),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)

    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
    return out

# Button class for the button size, postion and the text 
class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

# Empty list to append size and position, key or text wise  
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 150, 100 * i + 150], key))

# Infinite loop 
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = drawAll(img, buttonList)
 
    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size
 
            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                l, _, _ = detector.findDistance(8, 12, img, draw=False)
 
                # Double clicked
                if l < 30:
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    finalText += button.text
                    playsound('click.wav')
                    sleep(0.2)
 
    cv2.rectangle(img, (300, 500), (1000, 600), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (320, 580),
                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
 
    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) == 27:
        break

# Exit
cap.release()
cv2.destroyAllWindows()
