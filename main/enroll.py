from utils import Conf
from imutils.video import VideoStream
import sqlite3
import face_recognition
import argparse
import imutils
#import pyttsx3
import time
import cv2
import os
ids=input("Input The no: ")
name=input("Input the name of the person: ")
config_file="/home/pi/Desktop/Attendance Management System/config/config.json"
conf = Conf(config_file)

# initialize the database and student table objects
db = sqlite3.connect(conf["db_path"])

cur= db.cursor()
ids=(ids)
qry="Select * from employee where id="+ids+";"
# retrieve student details from the database
employee=cur.execute(qry).fetchall()
print(employee)
if len(employee) == 0:
    # initialize the video stream and allow the camera sensor to warmup
    print("[INFO] warming up camera...")
    vs = VideoStream(src=0).start()
    #vs = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)

# initialize the number of face detections and the total number of images saved to disk
    faceCount = 0
    total = 0
# the speech rate
    """ttsEngine = pyttsx3.init()
    ttsEngine.setProperty("voice", conf["language"])
    ttsEngine.setProperty("rate", conf["rate"])

    # ask the student to stand in front of the camera
    ttsEngine.say("{} please stand in front of the camera until you" \
                  "receive further instructions".format(name))
    ttsEngine.runAndWait()
    """
    status = "detecting"

 # create the directory to store the student's data
    os.makedirs(os.path.join(conf["dataset_path"],ids), exist_ok=True)
 # loop over the frames from the video stream
    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        frame = cv2.flip(frame, 1)
        orig = frame.copy()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb,
                model=conf["detection_method"])

 # loop over the face detections
        for (top, right, bottom, left) in boxes:
            cv2.rectangle(frame, (left, top), (right, bottom),(0, 255, 0), 2)
            if faceCount < conf["n_face_detection"]:
                faceCount += 1
                status = "detecting"
                
                

            p = os.path.join(conf["dataset_path"],
            ids, "{}.png".format(str(total).zfill(5)))
            cv2.imwrite(p, orig[top:bottom, left:right])
            total += 1
            status = "saving"
            cv2.putText(frame, "Status: {}".format(status), (10, 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            cv2.imshow("Frame", frame)
            cv2.waitKey(1)

        if total == conf["face_count"]:
    # let the student know that face enrolling is over
            #ttsEngine.say("Thank you {} you are now enrolled in the {} " \
            #"class.".format(name, conf["class"]))
            #ttsEngine.runAndWait()
            print("Thank you you have been enrolled")
            l=[(ids,name,"enrolled")]
            q2="Insert into entry (id,name,status) values(?,?,?);"        

            cur.executemany(q2,l)
            s=cur.execute("Select  * from entry;").fetchall()
            print(s)
            db.commit()
            
            print("[INFO] {} face images stored".format(total))
            print("[INFO] cleaning up...")
            break

# otherwise, a entry for the student id exists
    else:
        
 # get the name of the student
        name = "Select name from entry"
        print("[INFO] {} has already already been enrolled...".format(name))
cv2.destroyAllWindows()
vs.stop()
cur.close()
db.close()
