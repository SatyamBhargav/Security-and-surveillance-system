import face_recognition as f
import cv2
import sys
import _pickle as c

s, camera, name = sys.argv
def addfacepy(name):
    if camera == "on":
        cam = cv2.VideoCapture(0)
        while True:
            _, img1 = cam.read()
            img = cv2.flip(img1,1)
            cv2.imshow("Press 'a' to add your face", img)
            k = cv2.waitKey(10)
            if k == ord('a'):
                #face_enc = f.face_encodings(img_array)[0]
                file = './ImageDatabase/' + str(name)+ '.jpg'
                cv2.imwrite(file, img)
                #with open ("ImageDatabase/" + name, 'wb') as fp:
                #    c.dump(face_enc, fp)
                break
    print('done')
    cam.release()
    cv2.destroyAllWindows()

addfacepy(name)

