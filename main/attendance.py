..from utils import Conf
from imutils.video import VideoStream
from datetime import datetime
from datetime import date
#from tinydb import TinyDB
from tinydb import where
import face_recognition
import numpy as np
import argparse
import imutils
from imutils.video import FPS
#import pyttsx3
import sqlite3
import pickle
import time
import cv2
conf = Conf("/home/pi/Desktop/Attendance Management System/config/config.json")
db = sqlite3.connect(conf["db_path"])
cur=db.cursor()
 # load the actual face recognition model along with the label encoder
recognizer = pickle.loads(open(conf["recognizer_path"], "rb").read())
le = pickle.loads(open(conf["le_path"], "rb").read())
print("[INFO] warming up camera...")
vs = VideoStream(src=0).start()
#vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
fps = FPS().start()
# initialize previous and current person to None
prevPerson = None
curPerson = None

# initialize consecutive recognition count to 0
consecCount = 0

# initialize the text-to-speech engine, set the speech language, and
# the speech rate
print("[INFO] taking attendance...")
#ttsEngine = pyttsx3.init()
#ttsEngine.setProperty("voice", conf["language"])
#ttsEngine.setProperty("rate", conf["rate"])

# initialize a dictionary to store the student ID and the time at
# which their attendance was taken
studentDict = {}
logins=0
currentTime=datetime.now()
import datetime
nextday=(currentTime+datetime.timedelta(minutes=1)).strftime("%H:%M")
tommo=(currentTime+datetime.timedelta(days=1)).strftime("%D")
from datetime import datetime
while True:
# store the current time and calculate the time difference
# between the current time and the time for the class
    
 # grab the next frame from the stream, resize it and flip it
 # horizontally
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb,model=conf["detection_method"])
    import datetime
    today=datetime.datetime.now().strftime("%H:%M")
    today1=datetime.datetime.now().strftime("%D")
    
    from datetime import datetime
    currentTime=datetime.now()
    
    for (top, right, bottom, left) in boxes:
        cv2.rectangle(frame, (left, top), (right, bottom),(0, 255, 0), 2)
        #timeRemaining = conf["max_time_limit"] - timeDiff

    cv2.putText(frame, "Class: {}".format(conf["class"]), (10, 10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        #cv2.putText(frame, "Class timing: {}".format(conf["timing"]),(10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    cv2.putText(frame, "Current time: {}".format(
    currentTime.strftime("%H:%M:%S")), (10, 40),
    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        #cv2.putText(frame, "Time remaining: {}s".format(timeRemaining),(10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    if len(boxes) > 0:
        encodings = face_recognition.face_encodings(rgb, boxes)
        preds = recognizer.predict_proba(encodings)[0]
        j = np.argmax(preds)
        curPerson = le.classes_[j]
        if prevPerson == curPerson:
            consecCount += 1
        else:
            consecCount = 0
        prevPerson = curPerson
        if consecCount >= conf["consec_count"]:
            from datetime import datetime
            FMT = '%H:%M'
            
            query="Select name from entry where id="+curPerson+";"
            s=cur.execute(query).fetchall()
            for i in s:
                for j in i:
                    name=j
            query4="Select id from emp where id="+curPerson+";"
            m=cur.execute(query4).fetchall()
            if(m is None):
                logins=0
            query="Select time from emp where id="+curPerson+"  AND logger="+str(logins)+";"
            s=cur.execute(query).fetchall()
            if(s  is not None):
                for i in s:
                    for j in i:
                        nextday=j
            print(nextday)
            timeDiff=(datetime.strptime(nextday, FMT) - datetime.strptime(today, FMT)).seconds

            if(logins%2==0):
                if(logins==0):
                    logins+=1
                    s=(curPerson,today1,today,logins)
                    
                    query="Insert into emp (id,date,time,logger) values(?,?,?,?)"
                    cur.execute(query,s)
                    db.commit()
                    from datetime import datetime
                    studentDict[curPerson]=[datetime.now().strftime("%H:%M:%S"),logins]
                    print(studentDict) 
                    import datetime
                    nextday=(currentTime+datetime.timedelta(minutes=1)).strftime("%H:%M")
                    print(timeDiff)
                elif(logins!=0 and timeDiff>60):
                    query2="Select logger from emp where id="+curPerson+";"
                    s=cur.execute(query2).fetchall()
                    for i in s:
                        for j in i:
                            logins=j
                    logins=int(logins)
                    logins+=1
                    s=(curPerson,today1,today,logins)
                    
                    query="Insert into emp (id,date,time,logger) values(?,?,?,?)"
                    cur.execute(query,s)
                    db.commit()
                    
                    from datetime import datetime
                    
                    studentDict[curPerson]=[datetime.now().strftime("%H:%M:%S"),logins]
                    print(studentDict) 
                    import datetime
                    nextday=(currentTime+datetime.timedelta(minutes=1)).strftime("%H:%M")
                    print(timeDiff)
                            
            elif(logins %2==1 and timeDiff>60):
                query="Select logger from emp where id="+curPerson+";"
                s=cur.execute(query).fetchall()
                if(s is not None):
                    for i in s:
                        for j in i:
                            logins=j
                logins=int(logins)
                logins+=1
                s=(curPerson,today1,today,logins)
                    
                query="Insert into emp (id,date,time,logger) values(?,?,?,?)"
                cur.execute(query,s)
                db.commit()
                    
                from datetime import datetime
                studentDict[curPerson]=[datetime.now().strftime("%H:%M:%S"),logins]
                
                print(studentDict)
                
                import datetime
                nextday=(currentTime+datetime.timedelta(minutes=1)).strftime("%H:%M")
                print(nextday)
                
            if(today1==tommo):
                logins=0
                #name = studentTable.search(where(curPerson))[0][curPerson][0]
                #ttsEngine.say("{} your attendance has been taken.".format(name))
                #ttsEngine.runAndWait()
            label = "{}, you are now marked as present in {}".format(name, conf["class"])
               
            cv2.putText(frame, label, (5, 175),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)



        else:
            label = "Please stand in front of the camera"
            cv2.putText(frame, label, (5, 175),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
    cv2.imshow("Attendance System", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
print("[INFO] cleaning up...")
fps.stop()
vs.stop()

db.close()