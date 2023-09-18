import cv2
import pickle
import cvzone
import numpy as np
from pyrebase import pyrebase
from flask import Flask, render_template

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

app = Flask(__name__)

# ROUTE TO DISPLAY THE SPACE COUNTER ON A WEB PAGE
@app.route("/")
def index():
    space_counter = database.child("space_counter").get().val()
    return render_template("index.html", space_counter=space_counter)

if __name__ == "__main__":
    cap = cv2.VideoCapture('carPark.mp4')
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
    width, height = 107, 48
    prev_space_counter = None
    app.run(debug=True)
