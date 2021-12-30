import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


cap = cv2.VideoCapture("Muestra.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)
print('fps:'+str(fps))
index_list = [66,296,297,67] # Lista con posicione de puntos correspondientes a la frente
output_size = (130, 60) #Dimensiones de frame de solo la frente para posterior analisis en matlab
writer = cv2.VideoWriter('outpy.mp4',cv2.VideoWriter_fourcc('M','J','P','G'), 20, output_size) 
posiciones_frente = []




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
                for index in index_list: #Vamos seleccionando los puntos del poligono y guardando su posición en posiciones_frente
                    x = int(face_landmarks.landmark[index].x * width)
                    y = int(face_landmarks.landmark[index].y * height)
                    posiciones_frente.append([x,y])
        if not posiciones_frente: #El primer frame genera problemas por lo que se escoge una posicion promedio para este
            posiciones_frente = [[10,5],[20,30],[70,20],[50,10]] 
                   
        #Generamos la mascara correspondiente para poder obtener un frame solo de la frente 
        mask = np.zeros(frame.shape[0:2], dtype=np.uint8)
        points = np.array([posiciones_frente])
        cv2.drawContours(mask, [points], -1, (255, 255, 255), -1, cv2.LINE_AA)
        res = cv2.bitwise_and(frame,frame,mask = mask)
        rect = cv2.boundingRect(points) # returns (x,y,w,h) of the rect
        cropped = res[rect[1]: rect[1] + 60, rect[0]: rect[0] + 130]
    
   
        #Guardamos este frame en output.avi
        writer.write(cv2.resize(cropped, output_size))
        cv2.imshow("Cropped", cropped )
        posiciones_frente = []    
 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            writer.release()
            break

writer.release()
cv2.destroyAllWindows()

