from datetime import datetime
import cv2, pandas


first_frame = None
status_list = [None, None]
times = []
df = pandas.DataFrame(columns=["Start", "End"])
fourcc = cv2.VideoWriter_fourcc(*'XVID')
footage = cv2.VideoWriter("./2.Output_Files/Footage.mp4v", fourcc, 20.0, (640,480))
cap = cv2.VideoCapture(0)

while(cap.isOpened()):
    ret, frame1 = cap.read()
    status = 0
    text = 'Unoccupied'
    frame = cv2.flip(frame1,1)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(21,21),0)
    cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if first_frame is None:
        first_frame = gray
        continue

    delta_frame = cv2.absdiff(first_frame,gray)
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=0)
    cnts,_ = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) > 900:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x,y), (x+w,y+h),(0,255,0), 2)
            text = 'Occupied'
            continue
        status = 1
        

        
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, '{+} Frame Status: %s' % (text),(10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        #cv2.putText(frame, "Status: {}".format('Movement'), (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame, datetime.now().strftime('%A %d %B %Y %I:%M:%S%p'),(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255),1)  # frame.shape[0] = hieght, frame.shape[1] = width,ssssssssssssss
    status_list.append(status)

    status_list = status_list[-2:]

    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())

    cv2.imshow("Press 'Esc' to exit", frame)
    footage.write(frame)
    #cv2.imshow('Capturing', gray)
    #cv2.imshow('delta',delta_frame)
    #cv2.imshow('thresh', thresh_frame)

    key=cv2.waitKey(40)

    if key == 27:
        if status == 1:
            times.append(datetime.now())
        break

print(status_list)
print(times)

for i in range(0, len(times), 2):
    df = df.append({"Start": times[i], "End": times[i + 1]}, ignore_index=True)

df.to_csv("./2.Output_Files/Times.csv")

cap.release()
footage.release()
cv2.destroyAllWindows()