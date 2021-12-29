from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
from skimage import io
import argparse
import cv2
import mediapipe as mp
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd


def superpix (frame):
# apply SLIC and extract (approximately) the supplied number
# of segments
    segments = slic(frame, n_segments = 100, sigma = 5)
# show the output of SLIC
    fig = plt.figure("Superpixels -- %d segments%")
    ax = fig.add_subplot(1, 1, 1)
    ax.imshow(mark_boundaries(frame, segments))
    plt.axis("off")
    fig = plt.figure("Superpixels -- %d segments%")
    ax = fig.add_subplot(1, 1, 1)
    ax.imshow(mark_boundaries(frame, segments))
    plt.axis("off")
# show the plots
    plt.show(block=False)
    plt.pause(0.001)
    return 



mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
#cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap = cv2.VideoCapture("mzuniga1.MOV");
fps = cap.get(cv2.CAP_PROP_FPS)
print('fps:'+str(fps))
index_list = [66,296,297,67]

plt.ion()
xs = []
blue = []
red = []
green = []

b_frame = []
g_frame = []
r_frame = []
s_frame = []
frame_count = 0
second = 1

is_new_frame = False

posiciones_frente = []

def Average(lst):
    return sum(lst) / len(lst)

with mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    min_detection_confidence=0.5) as face_mesh:
    while True:
        ret, frame = cap.read()
        if ret == False:
            break
        frame = cv2.flip(frame,1)
        height, width, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame_rgb)
        if results.multi_face_landmarks is not None:
            for face_landmarks in results.multi_face_landmarks:
                for index in index_list:
                    x = int(face_landmarks.landmark[index].x * width)
                    y = int(face_landmarks.landmark[index].y * height)
                    cv2.circle(frame, (x, y), 2, (255, 0, 255), 2)
                    posiciones_frente.append([x,y])
        if not posiciones_frente:
            posiciones_frente = [[10,5],[20,30],[70,20],[50,10]] 
                   
        mask = np.zeros(frame.shape[0:2], dtype=np.uint8)
        points = np.array([posiciones_frente])
        mask = np.zeros(frame.shape[0:2], dtype=np.uint8)
        cv2.fillPoly(mask,[points],(255))
        img_poly = frame.copy()
        cv2.polylines(img_poly, [points], True, (0,0,255), 1)
        values = frame[np.where(mask == 255)]

        mask = np.zeros(frame.shape[0:2], dtype=np.uint8)
        points = np.array([posiciones_frente])
        cv2.drawContours(mask, [points], -1, (255, 255, 255), -1, cv2.LINE_AA)
        res = cv2.bitwise_and(frame,frame,mask = mask)
        rect = cv2.boundingRect(points) # returns (x,y,w,h) of the rect
        cropped = res[rect[1]: rect[1] + rect[3], rect[0]: rect[0] + rect[2]]
        wbg = np.ones_like(frame, np.uint8)*255
        cv2.bitwise_not(wbg,wbg, mask=mask)
        dst = wbg+res
        #cv2.imshow("Cropped", cropped )

        ROI_frame = img_as_float(cropped)
        #cv2.imshow("Cropped", cropped )
        superpix(ROI_frame)



        posiciones_frente = []  
        

        b ,g ,r = zip(*values)
       

        is_new_frame = True  # New frame has come

        

        

        s_frame.append(second)
        b_frame.append(Average(b))
        g_frame.append(Average(g))
        r_frame.append(Average(r))

        listaq = []
        listaq.append(b_frame)
        listaq.append(g_frame)
        listaq.append(r_frame)
        listaq.append(s_frame)
        pd.DataFrame({'a': listaq[0], 'b': listaq[1], 'c': listaq[2],'d': listaq[3]}).to_excel('output.xls', header = False, index = False) 

    
        #plt.plot(s_frame, b_frame, 'b', label='blue', lw=7)
        #plt.plot(s_frame, g_frame, 'g', label='green', lw=4)
        #plt.plot(s_frame, r_frame, 'r', label='red')
        #plt.xlabel('seconds')
        #plt.ylabel('mean')
        #if frame_count == 0:
            #plt.legend()
        #plt.draw()
        #plt.show(block=False)
       
           
        #plt.pause(0.001)
        second += 1
        
        
        #cv2.imshow('barn_poly', img_poly)
        #cv2.imshow("Frame", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            break


cv2.destroyAllWindows()

