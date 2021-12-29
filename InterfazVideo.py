import tkinter 
from tkinter import *
from tkinter import messagebox as MessageBox
import os
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2
import imutils


cap = None
   
def visualizarCaptura():
    
    global cap
    if cap is not None:      
        ret, frame = cap.read()
        if ret == True:
            frame = imutils.resize(frame, width=640)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            labelVideoCamara.configure(image=img)
            labelVideoCamara.image = img
            labelVideoCamara.after(10, visualizarCaptura)
        else:
            labelVideoCamara.image = ""
            cap.release()
            
def iniciarCaptura():
    global cap
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    visualizarCaptura()

def finalizarCaptura():
    global cap
    cap.release()




def seleccionar_visualizar():
    global cap
    if cap is not None:
        labelVideo.image = ""
        cap.release()
        cap = None
    video_path = filedialog.askopenfilename(filetypes = [
        ("all video format", ".mp4"),
        ("all video format", ".avi")])
    if len(video_path) > 0:
        labelVideoPath.configure(text=video_path)
        labelVideoPath.grid(column=1, row=10)
        cap = cv2.VideoCapture(video_path)
        visualizarVideo()
    else:
        labelVideoPath.configure(text="Aún no se ha seleccionado un video")
        labelVideoPath.grid(column=1, row=10)

def visualizarVideo():
    global cap
    if cap is not None:
        ret, frame = cap.read()
        if ret == True:
            frame = imutils.resize(frame, width=640)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            labelVideo.configure(image=img)
            labelVideo.image = img
            labelVideo.after(10, visualizarVideo)
        else:
            labelVideoPath.configure(text="Aún no se ha seleccionado un video")
            labelVideoPath.grid(column=1, row=10)
            labelVideo.image = ""
            cap.release()

archivo= open("Datos.txt","a")
if os.stat("Datos.txt").st_size == 0:
    archivo.write("Nombre-Edad-Presion\n")

if __name__ == "__main__":
    cap = None
    video = Tk()
    video.config(bg="lightblue")
    video.title("Video")
    video.geometry("1100x1100")
    video.config( bg="#49A")
    video.title("APPresion")

    #titulo
    titulo = Label(video, text="APPresion", font=("Arial",35),bg="lightblue")
    titulo.grid(column=0, row=0 , padx=10, pady=10)#,columnspan=0)

    
    labelrelleno7=Label(video, text="", bg="#49A")
    labelrelleno7.grid(column=0,row=1)


    #usuario
    nombrelabel=Label(video, text="Ingrese el nombre del paciente: ", bg="lightblue")
    nombrelabel.grid(column=0,row=2)

    labelrelleno=Label(video, text="", bg="#49A")
    labelrelleno.grid(column=0,row=3)

    edadlabel=Label(video, text= "Ingrese la edad del paciente", bg="lightblue")
    edadlabel.grid(column=0, row=4)

    labelrelleno2=Label(video, text="", bg="#49A")
    labelrelleno2.grid(column=0,row=5)

    labeltext=Label(video, text="Para poder importar el video haga click en el boton:", bg="lightblue")
    labeltext.grid(column=0,row=7)

    nombrePaciente= StringVar()
    edadPaciente= StringVar()
    
    NombreEntry= Entry(video, textvariable=nombrePaciente)
    NombreEntry.grid(column=1,row=2)
    nombrePaciente.set("Marcos Zuñiga")
    nombre=nombrePaciente.get()
    print(nombre)

    
    edadEntry= Entry(video, textvariable=edadPaciente)
    edadEntry.grid(column=1,row=4)
    edadPaciente.set("40")
    edad=edadPaciente.get()
    print(edad)
    archivo.write(nombre+" "+edad+"\n")
    
    #labelrelleno3=Label(video, text="", bg="#49A")
    #labelrelleno3.grid(column=0,row=7)

    botonVisualizar = Button(video , text="Importar video",width=15, command=seleccionar_visualizar)
    botonVisualizar.grid(column=1, row=7)
    buttonFinalizar2 = Button(video, text="Finalizar Importe", width=15, command=finalizarCaptura)
    buttonFinalizar2.grid(column=2, row=7)
    lblInfo1 = Label(video , text="Video de entrada:", bg="lightblue")
    lblInfo1.grid(column=0, row=10)
    labelVideoPath = Label(video , text="No se ha seleccionado un video", bg="lightblue")
    labelVideoPath.grid(column=1, row=10)
    labelrelleno4=Label(video, text="", bg="#49A")
    labelrelleno4.grid(column=0,row=11)
    labelVideo = Label(video,  bg="#49A" )
    labelVideo.grid(column=1, row=16)

    lbl1 = Label(video , text="Video/Captura :", bg="lightblue")
    lbl1.grid(column=0, row=15)

    labelrelleno8=Label(video, text="", bg="#49A")
    labelrelleno8.grid(column=0,row=14)

    labelVideoPath = Label(video , text="Para utilizar la camara :", bg="lightblue")
    labelVideoPath.grid(column=0, row=13)

    labelVideoPath = Label(video , text="Para utilizar la camara :", bg="lightblue")
    labelVideoPath.grid(column=0, row=13)

    buttonIniciar = Button(video, text="Iniciar Captura", width=15, command=iniciarCaptura)
    buttonIniciar.grid(column=1, row=13)
    buttonFinalizar = Button(video, text="Finalizar Captura", width=15, command=finalizarCaptura)
    buttonFinalizar.grid(column=2, row=13)
    labelVideoCamara = Label(video,bg="#49A")
    labelVideoCamara.grid(column=1, row=16, columnspan=2)
    labelrelleno6=Label(video, text="", bg="#49A")
    labelrelleno6.grid(column=0,row=9)
    video.mainloop()
    

    #botonGuardar = Button(video , text="guardar", command=)
    #botonGuardar.grid(column=1, row=5, padx=5, pady=5, columnspan=2)
    video .mainloop()