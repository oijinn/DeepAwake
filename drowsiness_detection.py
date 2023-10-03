import cv2
import os
from keras.models import load_model
import numpy as np
from pygame import mixer
import time
from gui import *
import threading
import ctypes

user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)


def start_detection():
    mixer.init()
    
    sound = mixer.Sound('alarm.wav')
    
    last_update_time = time.time()
    face_cascade = cv2.CascadeClassifier('haar cascade files\haarcascade_frontalface_alt.xml')
    lefteye_cascade = cv2.CascadeClassifier('haar cascade files\haarcascade_lefteye_2splits.xml')
    righteye_cascade = cv2.CascadeClassifier('haar cascade files\haarcascade_righteye_2splits.xml')

    labels=['Close','Open']

    model = load_model('models/CNN_drowsi.h5')
    path = os.getcwd()
    cap = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    count=0
    score=0
    max_score = 30
    thickness=2
    left_predictions=[99]
    right_predictions=[99]
    while(True):
        ret, frame = cap.read()
        height,width = frame.shape[:2] 

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        face = face_cascade.detectMultiScale(gray,minNeighbors=5,scaleFactor=1.3,minSize=(25,25))
        left_eye = lefteye_cascade.detectMultiScale(gray)
        right_eye = righteye_cascade.detectMultiScale(gray)

        cv2.rectangle(frame, (0,height-50) , (200,height) , (255,255,204) , thickness=cv2.FILLED )

        for (x,y,w,h) in face:
            cv2.rectangle(frame, (x,y) , (x+w,y+h) , (100,100,100) , 1 )

        for (x,y,w,h) in left_eye:
            leye=frame[y:y+h,x:x+w]
            count=count+1
            leye = cv2.cvtColor(leye,cv2.COLOR_BGR2GRAY)
            leye = cv2.resize(leye,(24,24))
            leye= leye/255
            leye=  leye.reshape(24,24,-1)
            leye = np.expand_dims(leye,axis=0)
            left_predictions = np.argmax(model.predict(leye), axis=-1)
            if(left_predictions[0]==1):
                labels='Open' 
            if(left_predictions[0]==0):
                labels='Closed'
            break

        for (x,y,w,h) in right_eye:
            reye=frame[y:y+h,x:x+w]
            count=count+1
            reye = cv2.cvtColor(reye,cv2.COLOR_BGR2GRAY)
            reye = cv2.resize(reye,(24,24))
            reye= reye/255
            reye=  reye.reshape(24,24,-1)
            reye = np.expand_dims(reye,axis=0)
            right_predictions = np.argmax(model.predict(reye), axis=-1)
            if(right_predictions[0]==1):
                lbl='Open' 
            if(right_predictions[0]==0):
                lbl='Closed'
            break

        if(left_predictions[0]==0 and right_predictions[0]==0):
            score=min(score+1, max_score)
            cv2.putText(frame,"Closed",(10,height-20), font, 1,(0,0,0),1,cv2.LINE_AA)
        else:
            score=min(score-1, max_score)
            cv2.putText(frame,"Open",(10,height-20), font, 1,(0,0,0),1,cv2.LINE_AA)
        
        # Dashboard
        current_time = time.time()
        if current_time - last_update_time >= 1:
            last_update_time = current_time
            scores.append(score)
            if (len(times) == 0):
                times.append(0)
            else:
                times.append(times[-1] + 1)
            update_series_graph()
            update_bar_graph()
            
        if(score<0):
            score=0   
        cv2.putText(frame,'Score:'+str(score),(100,height-20), font, 1,(0,0,0),1,cv2.LINE_AA)
        if(score>15):
            #alarm is played when driver is detected drowsy
            cv2.imwrite(os.path.join(path,'image.jpg'),frame)
            try:
                sound.play()
            except:  # is playing = False
                pass
            if(thickness<16):
                thickness= thickness+2
            else:
                thickness=thickness-2
                if(thickness<2):
                    thickness=2
            cv2.rectangle(frame,(0,0),(width,height),(0,0,255),thickness) 
        
        camera_window_name = "Camera"
        cv2.namedWindow(camera_window_name, cv2.WND_PROP_AUTOSIZE)
        cv2.imshow(camera_window_name, frame)
        
        x = (screen_width - width) // 2
        y = screen_height - height - 100
        cv2.moveWindow(camera_window_name, x, y)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


thread = threading.Thread(target=start_detection, daemon=True)
thread.start()
start_gui()