import tkinter 
from tkinter import *
from tkinter import messagebox as MessageBox
import os
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
import time


#Funcion encargada de mostrar la imagen que capta la camara
cap = None
#Funcion encargada de  
def visualizarCaptura():
    global cap
    #Si no es vacia
    if cap is not None:   
        #Se lee   
        ret, frame = cap.read()
        if ret == True:
            #Se escribe el frame
            writer.write(frame)
            #Se define el tamaño
            frame = imutils.resize(frame, width=640)
            #Le entrega el fondo base
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            labelVideoCamara.configure(image=img)
            labelVideoCamara.image = img
            labelVideoCamara.after(10, visualizarCaptura)
        else:
            labelVideoCamara.image = ""
            cap.release()

#Funcion que inicia la captura de imagenes que va entregando la camara       
def iniciarCaptura():
    #Funciones globales
    global cap
    global writer
    global width
    global height
    #Inicia la captura del video
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #Se crea el video con el formato "Muestra.mp4"
    writer= cv2.VideoWriter('Muestra.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 20, (width,height))
    #Se genera un ciclo
    visualizarCaptura()
   
#Funcion encargada de terminar el proceso de grabacion de la camara
def finalizarCaptura():
    #funciones globales
    global cap
    global writer
    global labelVideoCamara
    #Se libera lo almacenado
    cap.release()
    writer.release()
    #Se destruyen los siguientes elementos, esto genera luego una dependencia de orden al momento de usar la interfaz
    #Se podra solamente Grabar y luego importar o Importar, hacerlo en otro orden y mas de una vez el proceso hara que no funcione
    #Esto se hizo debido a que la ventana de la camara se superponia a la ventana del import tras haber sido llamado antes, entonces
    #tuvo que ser eliminada para que se pudiera ver el video
    labelVideoCamara.destroy()
    buttonIniciar.destroy()
    buttonFinalizar.destroy()
    labelVideoCamara.destroy()




#Funcion encargada de abrir el archivo que se querra importar
def seleccionar_visualizar():
    global cap
    #Si cap no es vacio
    if cap is not None:
        labelVideo.image = ""
        #Se libera
        cap.release()
        cap = None
    #Se abre el archivo
    video_path = filedialog.askopenfilename(filetypes = [
        #permite formato .mp4 , .avi y .mod
        ("all video format", ".mp4"),
        ("all video format", ".mod"),
        ("all video format", ".avi")])
    #Si se selecciono el video   
    if len(video_path) > 0:
        #Muestra el video
        labelVideoPath.configure(text=video_path)
        labelVideoPath.grid(column=1, row=10)
        cap = cv2.VideoCapture(video_path)
        #Bucle
        visualizarVideo()
    #Si no se selecciono un video
    else:
        labelVideoPath.configure(text="Aún no se ha seleccionado un video")
        labelVideoPath.grid(column=1, row=10)

#Muestra el video importado
def visualizarVideo():
    global cap
    #Ayuda en la velocidad de reproduccion del video, sin esto se reproducian a mucha velocidad
    time.sleep(0.15)
    #si cap no es vacio
    if cap is not None:
        #Se lee
        ret, frame = cap.read()
        if ret == True:
            #Define el tamaño del frame
            frame = imutils.resize(frame, width=640)
            #Se define un color
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            labelVideo.configure(image=img)
            labelVideo.image = img
            labelVideo.after(10, visualizarVideo)
        
        #En caso que no se selecciono un video
        else:
            labelVideoPath.configure(text="Aún no se ha seleccionado un video")
            labelVideoPath.grid(column=1, row=10)
            labelVideo.image = ""
            cap.release()

#Crea un archivo .txt en donde se guardara el nombre y la edad del paciente
archivo= open("Datos.txt","a")
#Si el archivo esta vacio entonces se escribe el resultado
if os.stat("Datos.txt").st_size == 0:
    archivo.write("Nombre-Edad-Presion\n")


if __name__ == "__main__":
    cap = None
    #Se crea la ventana con tkinter llamada "video"
    video = Tk()
    #Le entrega un fondo de color "#49A"
    video.config(bg="#49A")
    #Le pone en la barra superior el nombre video (a la ventana)
    video.title("APPresion")
    #Define las medidas de la ventana (tamaño)
    video.geometry("1100x1100")

    #titulo, muestra el APPresion 
    titulo = Label(video, text="APPresion", font=("Arial",35),bg="lightblue")
    #Define su posicion
    titulo.grid(column=0, row=0 , padx=10, pady=10)#,columnspan=0)




    # Seccion que se relacion con la interfaz que pide los datos al usuario
    nombrePaciente= StringVar()
    edadPaciente= StringVar()
    
    nombrelabel=Label(video, text="Ingrese el nombre del paciente: ", bg="lightblue")
    nombrelabel.grid(column=0,row=2)

    edadlabel=Label(video, text= "Ingrese la edad del paciente", bg="lightblue")
    edadlabel.grid(column=0, row=4)

    labeltext=Label(video, text="Para poder importar el video haga click en el boton:", bg="lightblue")
    labeltext.grid(column=0,row=7)

    #Labels de relleno, simulan un espacio, es para el orden
    labelrelleno=Label(video, text="", bg="#49A")
    labelrelleno.grid(column=0,row=3)

    labelrelleno2=Label(video, text="", bg="#49A")
    labelrelleno2.grid(column=0,row=5)


    #Crea las cajas de ingresar texto para el nombre del usuario
    NombreEntry= Entry(video, textvariable=nombrePaciente)
    NombreEntry.grid(column=1,row=2)
    #Pone un texto automatico en la casilla
    nombrePaciente.set("Marcos Zuñiga")
    nombre=nombrePaciente.get()
    print(nombre)

    #Crea las cajas de ingresar texto para la edad del usuario  
    edadEntry= Entry(video, textvariable=edadPaciente)
    edadEntry.grid(column=1,row=4)
    #Pone un texto automatico en la casilla
    edadPaciente.set("40")
    edad=edadPaciente.get()
    print(edad)

    #Se agrega al block de notas el nombre y la edad del paciente
    archivo.write(nombre+" "+edad+"\n")

    #Botones:
    #Boton que hace la conexion con la funcion seleccionar_visualizar 
    botonVisualizar = Button(video , text="Importar video",width=15, command=seleccionar_visualizar)
    #Estara posicionado en la columna 1 y fila 7
    botonVisualizar.grid(column=1, row=7)
    #Boton que se conecta a la funcion finalizarCaptura
    buttonFinalizar2 = Button(video, text="Finalizar Importe", width=15, command=finalizarCaptura)
    buttonFinalizar2.grid(column=2, row=7)
    #Boton que se conecta a la funcion iniciarCaptura, esta se relaciona con la captura con camara de un video
    buttonIniciar = Button(video, text="Iniciar Captura", width=15, command=iniciarCaptura)
    buttonIniciar.grid(column=1, row=13)
    #Boton que se encarga de terminar la grabacion en vivo
    buttonFinalizar = Button(video, text="Finalizar Captura", width=15, command=finalizarCaptura)
    buttonFinalizar.grid(column=2, row=13)


    #Labels, muestran textos en la interfaz grafica, en diferentes posiciones
    #Label que muestra el texto "Video entrada"
    lblInfo1 = Label(video , text="Video de entrada:", bg="lightblue")
    lblInfo1.grid(column=0, row=10)

    labelVideoPath = Label(video , text="No se ha seleccionado un video", bg="lightblue")
    labelVideoPath.grid(column=1, row=10)

    labelVideo = Label(video,  bg="#49A" )
    labelVideo.grid(column=1, row=16)

    lbl1 = Label(video , text="Video/Captura :", bg="lightblue")
    lbl1.grid(column=0, row=15)

    labelVideoPath = Label(video , text="Para utilizar la camara :", bg="lightblue")
    labelVideoPath.grid(column=0, row=13)

    labelVideoCamara = Label(video,bg="#49A")
    labelVideoCamara.grid(column=1, row=16, columnspan=2)

    #Labels de relleno, solo ocupan ese espacio, para generar un efecto de separacion, estan vacios
    labelrelleno4=Label(video, text="", bg="#49A")
    labelrelleno4.grid(column=0,row=11)

    labelrelleno8=Label(video, text="", bg="#49A")
    labelrelleno8.grid(column=0,row=14)

    labelrelleno6=Label(video, text="", bg="#49A")
    labelrelleno6.grid(column=0,row=9)
        
    labelrelleno7=Label(video, text="", bg="#49A")
    labelrelleno7.grid(column=0,row=1)

    #Para que la ventana continue abierta
    video.mainloop()
