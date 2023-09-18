# # IMPORTING NECESSARY LIBRARIES
# import cv2
# import pickle
# import cvzone
# import numpy as np
# from pyrebase import pyrebase
# import streamlit as st

# st.title("CAR PARKING")

# # FIREBASE CONFIG
# firebaseConfig = {
#  

# # INITIALIZING FIREBASE
# firebase = pyrebase.initialize_app(firebaseConfig)
# database = firebase.database()

# # FUNCTION TO CHECK FOR PARKING SPACES
# def checkParkingSpace(imgPro):
#     spaceCounter = 0

#     for pos in posList:
#         x,y = pos
#         imgCrop = imgPro[y:y+height,x:x+width]
#         count = cv2.countNonZero(imgCrop)
#         cvzone.putTextRect(img,str(count),(x,y+height-3), scale = 1, thickness=2, offset=0)

#         if count <800:
#             color = (0,255,0)
#             thickness = 5
#             spaceCounter +=1

#         else:
#             color = (0,0,255)
#             thickness = 2
#         cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height),color, thickness)

#     cvzone.putTextRect(img, f'FREE: {spaceCounter}/{len(posList)}', (100,50), scale=5, thickness=5, offset=20, colorR=(0,200,0) )

#     global prev_space_counter
#     if spaceCounter != prev_space_counter:
#         # database.push({"space_counter": spaceCounter})
#         database.update({"space_counter": spaceCounter})
#         print(spaceCounter)
#         prev_space_counter = spaceCounter
#         st.text(f"Number of free parking spaces: {spaceCounter}")

# # VIDEO FEED
# cap = cv2.VideoCapture('carPark.mp4')

# with open('CarParkPos', 'rb') as f:
#     posList = pickle.load(f)

# width, height = 107, 48

# prev_space_counter = None

# while True:
    # if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
    #     cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    # success, img = cap.read()
    # imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    # imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    #                                      cv2.THRESH_BINARY_INV, 25, 16)
    # imgMedian = cv2.medianBlur(imgThreshold,5)
    # kernal = np.ones((3, 3), np.uint8)
    # imgDilate = cv2.dilate(imgMedian, kernal, iterations=1)

    # checkParkingSpace(imgDilate)

    # cv2.imshow("image",img)
    # cv2.waitKey(3)

############### NEW CODE FROM CHATGPT #################
# IMPORTING NECESSARY LIBRARIES
import cv2
import pickle
import cvzone
import numpy as np
from pyrebase import pyrebase

# FIREBASE CONFIG
firebaseConfig = {
  "apiKey": 
  "authDomain":
  "databaseURL": 
  "projectId": 
  "storageBucket": 
  "messagingSenderId": 
  "appId": 
  "measurementId": 
}

# INITIALIZING FIREBASE
firebase = pyrebase.initialize_app(firebaseConfig)
database = firebase.database()

# FUNCTION TO CHECK FOR PARKING SPACES
def checkParkingSpace(imgPro):
    spaceCounter = 0

    for pos in posList:
        x,y = pos
        imgCrop = imgPro[y:y+height,x:x+width]
        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img,str(count),(x,y+height-3), scale = 1, thickness=2, offset=0)

        if count <800:
            color = (0,255,0)
            thickness = 5
            spaceCounter +=1

        else:
            color = (0,0,255)
            thickness = 2
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height),color, thickness)

    cvzone.putTextRect(img, f'FREE: {spaceCounter}/{len(posList)}', (100,50), scale=5, thickness=5, offset=20, colorR=(0,200,0) )

    global prev_space_counter
    if spaceCounter != prev_space_counter:
        # database.push({"space_counter": spaceCounter})
        database.update({"space_counter": spaceCounter})
        print(spaceCounter)
        prev_space_counter = spaceCounter

# VIDEO FEED
cap = cv2.VideoCapture('carPark.mp4')

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width, height = 107, 48


prev_space_counter = None

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold,5)
    kernal = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernal, iterations=1)

    checkParkingSpace(imgDilate)

    cv2.imshow("image",img)
    cv2.waitKey(3)
