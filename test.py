from tinydb import TinyDB
from tinydb import Query
import json
from tinydb import where
db=TinyDB("/home/pi/Desktop/Attendance Management System/database/database.json")
f=open("/home/pi/Desktop/Attendance Management System/database/database.json")
data =json.load(f)
for i in data["student"]:
    print(i)

