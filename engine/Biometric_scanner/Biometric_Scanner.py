import cv2
import numpy as np
import face_recognition
import os, csv
from datetime import datetime
from pathlib import Path

 
path = 'ImageDatabase'  # path of the folder where all sample images are present
images = []     # an empyt array
classNames = []
myList = os.listdir(path)   # it will fetch the name of the images ex - [Alba Test.jpg, Alba.jpg, Gal Gadot.jpg, Lulu.jpg]
print(myList)

# this loop will fetch image name from fath folder and append it to the array(classNames)

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0]) 
    # we dont want Name like - Alba.jpg,
    # we just want Alba so we use split function on the name an then reciving the first index 
    # i.e. only "Alba" and removing .jpg 
print(classNames)

# Meaning of Encoding
# Encoding is the process of converting data from one form to another.
# By encoding digital audio, video, and image files, they can be saved in a more efficient, compressed format. 
# Encoded media files are typically similar in quality to their original uncompressed counterparts, but have much smaller file sizes

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
 

def check_dir():
    file_path = Path("./1.Entry")
    csv_file = 'EntryData_' + str(datetime.now().strftime('%d_%m_%Y')) + '.csv' # it will include the current date of the system in the file name
    csv_file_full = file_path / csv_file
    if csv_file_full.is_file():
        direxist = csv_file_full
        #print('file exist')
        return direxist
    else:
        with open(csv_file_full,'w', newline='') as cd:
            header = ['Name', 'Time']
            writer = csv.writer(cd,delimiter=',')
            writer.writerow(header)
            dircreated = csv_file_full
            #print('just created')
            return dircreated

 # this function will check for filename (csv_file) in the following dir (file_path)
 # if it will find the file it will return the full path of the file (cvs_file_full)
 # and if not it will creat one and then return the full path of the file


 
def Biometric_scan(name):
    filename = check_dir()
    with open(filename,'r+') as f:  # r+ == reading and writing the file at same time
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')
 
encodeListKnown = findEncodings(images)
print('Encoding Complete')
 
cap = cv2.VideoCapture(0)
 
while True:
    success, img1 = cap.read()
    img = cv2.flip(img1,1)
    imgS = cv2.resize(img,(0,0),None,0.25,0.25) # reducing the size of the image by one forth
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    
    facesCurFrame = face_recognition.face_locations(imgS)  # facesCurFrame == faces in our current frame
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame) # encodesCurFrame == encoding in our current frame
    
    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        #print(faceDis)
        matchIndex = np.argmin(faceDis)
    
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            #print(name)
            Biometric_scan(name)
        if faceDis[matchIndex]< 0.60:
            Biometric_scan(name)
        else: 
            name = 'Unknown'
            #print(name)
        if name == 'Unknown':
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            # as we have resize our image in line 84, so if we want the rectangle around the face to be align properly,
            # we have to multiply the coordinates by 4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,0,255),cv2.FILLED) 
            # it will create a rectangular box under the frace box which will show the name. y-35 - it is for decreasing the lenght of the box/rectangle
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2) 
            # (x1+6,y2-6) - for aligning the text in to the small box which will show the name
        else:
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

    cv2.imshow('Biometric_scan Cam',img)
    key = cv2.waitKey(1)
    if key == 27:
        break
cv2.destroyAllWindows()
