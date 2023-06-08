#importing required modules
import tkinter
import customtkinter
from tkinter import *
from PIL import ImageTk,Image,ImageDraw
from random_username.generate import generate_username
import uuid
import requests
import mss.tools
import serial 
import os
import time
import pandas as pd
import requests
from scipy import signal
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table
from reportlab.lib import colors


try:
    os.remove("out_data/data.txt")
except:
    print("Data.txt no existe")


customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('blue')
app = customtkinter.CTk()
app1 = customtkinter.CTk()
wdth = app.winfo_screenwidth()
hgt = app.winfo_screenheight()
app.geometry("%dx%d"%(wdth,hgt))
app1.geometry("%dx%d"%(wdth,hgt))



start_frame=customtkinter.CTkFrame(master=app)
login_frame=customtkinter.CTkFrame(master=app)
registrar_frame=customtkinter.CTkFrame(master=app)
registrar_next_frame=customtkinter.CTkFrame(master=app)
bienvenido_frame=customtkinter.CTkFrame(master=app)
results_frame=customtkinter.CTkFrame(master=app)
final_frame=customtkinter.CTkFrame(master=app)
start_frame.pack()
spiral_tutorial_frame=customtkinter.CTkFrame(master=app)
spiral2_tutorial_frame=customtkinter.CTkFrame(master=app)
meander_tutorial_frame=customtkinter.CTkFrame(master=app)



imgs = Image.new('RGB',(500,500),(255,255,255))
imgs2 = Image.new('RGB',(500,500),(255,255,255))
imgm = Image.new('RGB',(500,500),(255,255,255))
imgc = Image.new('RGB',(960,229),(255,255,255))
draw = ImageDraw.Draw(imgs)
draw1 = ImageDraw.Draw(imgm)
draw2 = ImageDraw.Draw(imgc)
draw3 = ImageDraw.Draw(imgs2)

image_spiral = Image.open(r"templates/espiral.png")
image_spiral = image_spiral.resize((500,500))
image_meander = Image.open(r"templates/meander.png")
image_meander = image_meander.resize((500,500))
image_circle = Image.open(r"templates/wave_50.png")
bg1= ImageTk.PhotoImage(image_spiral)
bg2= ImageTk.PhotoImage(image_meander)
bg3= ImageTk.PhotoImage(image_circle)


mousePressed = False
last=None
index_aux=0
counter=4
state=True
predictions=['PD','HC','HC','HC','PD','PD','nan','nan']
porcentajes=['nan','nan','nan','nan','nan','nan','nan','nan']
def button_function():
    start_frame.pack_forget()            # destroy current window and creating new one 
    w = customtkinter.CTk()  
    w.geometry("1280x720")
    w.title('Welcome')
    l1=customtkinter.CTkLabel(master=w, text="Home Page",font=('Century Gothic',60))
    l1.place(relx=0.5, rely=0.5,  anchor=tkinter.CENTER)
    w.mainloop()
    


#*********************************************************INICIO DE INTERFAZ
img1 = customtkinter.CTkImage(Image.open("templates/login.jpg"), size=(wdth,hgt))
l1=customtkinter.CTkLabel(master=start_frame,image=img1,text='')
l2=customtkinter.CTkLabel(master=login_frame,image=img1)
l3=customtkinter.CTkLabel(master=registrar_frame,image=img1)
l4=customtkinter.CTkLabel(master=registrar_next_frame,image=img1)
l5=customtkinter.CTkLabel(master=bienvenido_frame,image=img1, text='')
l12=customtkinter.CTkLabel(master=final_frame,image=img1)
l13=customtkinter.CTkLabel(master=results_frame,image=img1,text='')
l1.pack()
l2.pack()
l3.pack()
l4.pack()
l5.pack()
l12.pack()
l13.pack()
scrollable_frame = customtkinter.CTkScrollableFrame(master=l13, width=700, height=250)
scrollable_frame2 = customtkinter.CTkScrollableFrame(master=l13, width=700, height=250)

header_names=['miliseg','AcX','AcY','AcZ','GyX','GyY','GyZ']

# Variables para el suavizado
smooth_factor = 0.3
last_point = None
smoothed_points = []

def start_drawing(event):
    global last_point
    last_point = (event.x, event.y)
    smoothed_points.append(last_point)

def continue_drawing(event):
    global last_point
    current_point = (event.x, event.y)
    smoothed_point = (
        int(last_point[0] + smooth_factor * (current_point[0] - last_point[0])),
        int(last_point[1] + smooth_factor * (current_point[1] - last_point[1]))
    )
    smoothed_points.append(smoothed_point)

    # Dibujar una línea suavizada
    if len(smoothed_points) >= 4:
        canvas.create_line(smoothed_points[-4:],fill="blue", smooth=True,width=3)
        draw.line(smoothed_points[-4:], fill="black", width=2)

    last_point = smoothed_point

def stop_drawing(event):
    global last_point
    last_point = None
    smoothed_points.clear() 

def press(evt):
    global mousePressed
    mousePressed = True
def release(evt):
    global mousePressed
    mousePressed = False

def move(evt):
    global mousePressed, last
    x,y = evt.x,evt.y
    if mousePressed:
        if last is None:
            last = (x,y)
            return
        draw.line(((x,y),last), (0,0,0))
        cvs.create_line(x,y,last[0],last[1],fill='blue',width=4,smooth=True, splinesteps=200)
        last = (x,y)
    else:
        last = (x,y)

def axis_images(filename,name):
    data = pd.read_csv(filename)
    t=data['miliseg'].values
    signal_x = data['AcX'].values
    signal_y = data['AcY'].values
    signal_z = data['AcZ'].values
    
    counter_here=0
    index=0
    down=0
    up=len(t)

    for i in t:
        t[index]=counter_here
        index=index+1
        counter_here=counter_here+20

    max_x=np.max(signal_x)
    max_y=np.max(signal_y)
    max_z=np.max(signal_z)
    min_x=np.min(signal_x)
    min_y=np.min(signal_y)
    min_z=np.min(signal_z)
    x_max=max_x+0.5
    y_max=max_y+0.5
    z_max=max_z+0.5
    x_min=min_x-0.5
    y_min=min_y-0.5
    z_min=min_z-0.5

    if len(t)>200:
        up=150
        down=50
    sns.set_style('darkgrid')
    plt.figure(figsize=(10, 4))
    plt.plot(t[down:up],signal_x[down:up], linewidth=1, label='Aceleración eje X')
    plt.plot(t[down:up],signal_y[down:up], linewidth=1, label='Aceleración eje Y')
    plt.plot(t[down:up],signal_z[down:up], linewidth=1, label='Aceleración eje Z')
    plt.xlabel('milisegundos')
    plt.ylabel('m/s2')
    plt.legend()
    plt.savefig('out_images/'+name+'.jpg')

def ingresar():
    start_frame.pack_forget()  
    login_frame.pack()
    app.state(newstate='withdraw')
    app.state(newstate='normal')
    #creating custom frame
    frame=customtkinter.CTkFrame(master=l2, width=320, height=360, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    ll1=customtkinter.CTkLabel(master=frame, text="Ingresar",font=('Century Gothic',20))
    ll1.place(x=110, y=45)

    entryl1=customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Nombre de usuario (CI)')
    entryl1.place(x=50, y=110)

    entryl2=customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Contrasena', show="*")
    entryl2.place(x=50, y=165)
    #Create custom button
    buttonl1 = customtkinter.CTkButton(master=frame, width=220, text="Ingresar", command=button_function, corner_radius=6)
    buttonl1.place(x=50, y=240)

def pagina_principal():
    results_frame.pack_forget()
    start_frame.pack()

def reporte():
    global name_var, ape_var, ci_var, fecha_var, predictions
    results_hc=[]
    results_pd=[]
    for i in predictions:
        if i=="HC":
            results_hc.append('si')
            results_pd.append('no')
        else:
            results_hc.append('no')
            results_pd.append('si')
    # Crear un objeto Canvas PDF
    pdf_canvas = canvas.Canvas("documento.pdf", pagesize=letter)
    
    # Agregar el contenido al PDF
    pdf_canvas.setFont("Helvetica", 8)
    pdf_canvas.drawString(50, 750, "Nombre completo: Ana Martinez")
    pdf_canvas.drawString(50, 730, "Apellido completo: Martinez ca")
    pdf_canvas.drawString(50, 710, "Documento de identidad: 123456789")
    pdf_canvas.drawString(50, 690, "Fecha de nacimiento: 01/01/2000")
    
    pdf_canvas.drawString(50, 670, "Patrones realizados:")
    
    # Agregar imágenes en dos filas
    y_position = 550  # Posición inicial en y
    y_position2 = 400
    # Fila de imágenes
    pdf_canvas.drawImage("templates/espiral.png", 50, y_position, width=100, height=100)
    pdf_canvas.drawImage("templates/espiral.png", 200, y_position, width=100, height=100)
    pdf_canvas.drawImage("templates/espiral.png", 350, y_position, width=100, height=100)
    pdf_canvas.drawImage("templates/espiral.png", 500, y_position, width=100, height=100)

    pdf_canvas.drawString(50, 530, "Evaluaciones de temblor")
    pdf_canvas.drawImage("templates/espiral.png", 50, y_position2, width=150, height=100)
    pdf_canvas.drawImage("templates/espiral.png", 350, y_position2, width=150, height=100)

    # Agregar tabla de 5 filas y 3 columnas
    data = [['Patron', 'sin sintomas motores', 'sintomas motores'],
            ['Espiral guiada', str(results_hc[0]), str(results_pd[0])],
            ['Espiral libre', str(results_hc[1]), str(results_pd[1])],
            ['Meandro guiado', str(results_hc[2]), str(results_pd[2])],
            ['Sinusoidal libre', str(results_hc[3]), str(results_pd[3])]]
    
    table = Table(data, colWidths=100, rowHeights=20)
    table.setStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Texto de la primera fila en negrita
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Centrar el texto en todas las celdas
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Centrar verticalmente el texto en todas las celdas
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Color del texto de la primera fila
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Agregar bordes a todas las celdas
        ('SIZE', (0, 0), (-1, -1), 8)])
    
    pdf_canvas.setFillColor(colors.blue)
    pdf_canvas.drawString(50, 380, "Resultados evaluacion de escritura:")    
    table.wrapOn(pdf_canvas, 200, 400)
    table.drawOn(pdf_canvas, 50, 250)

   # Agregar tabla de 5 filas y 3 columnas
    data2 = [['Evaluacion', 'Temblor', 'Frecuencia', 'Amplitud (m/s2)2/Hz'],
            ['Temblor postural', 'sin temblor','50','0.323'],
            ['Temblor en reposo', 'con temblor', '23','asd']]
    
    table2 = Table(data2, colWidths=100, rowHeights=20)
    table2.setStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Texto de la primera fila en negrita
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Centrar el texto en todas las celdas
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Centrar verticalmente el texto en todas las celdas
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Color del texto de la primera fila
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Agregar bordes a todas las celdas
        ('SIZE', (0, 0), (-1, -1), 8)])
    
    pdf_canvas.setFillColor(colors.blue)
    pdf_canvas.drawString(50, 220, "Resultados evaluacion de temblor:") 
    table2.wrapOn(pdf_canvas, 200, 400)
    table2.drawOn(pdf_canvas, 50, 150)
    
    # Guardar el PDF
    pdf_canvas.save()

def resultados():
    global predictions, porcentajes
    final_frame.destroy()
    #start_frame.pack_forget()
    results_frame.pack()
    img1_result = customtkinter.CTkImage(Image.open("out_images/spiral_img.jpg"), size=(250,250))
    img2_result = customtkinter.CTkImage(Image.open("out_images/spiral_trace.jpg"), size=(250,250))
    img3_result = customtkinter.CTkImage(Image.open("out_images/spiral2_img.jpg"), size=(250,250))
    img4_result = customtkinter.CTkImage(Image.open("out_images/meander_img.jpg"), size=(250,250))
    img5_result = customtkinter.CTkImage(Image.open("out_images/wave.jpg"), size=(350,250))
    img6_result = customtkinter.CTkImage(Image.open("out_images/point.jpg"), size=(350,250))
    img7_result = customtkinter.CTkImage(Image.open("out_images/reposo.jpg"), size=(350,250))
    

    scrollable_frame.place(anchor='nw')
    scrollable_frame2.place(rely=1,anchor='sw')
    image1=customtkinter.CTkFrame(master=scrollable_frame,height=250)
    image1.pack(fill='x', pady=(10, 20))
    image2=customtkinter.CTkFrame(master=scrollable_frame,height=250)
    image2.pack(fill='x', pady=(10, 20))
    image3=customtkinter.CTkFrame(master=scrollable_frame,height=250)
    image3.pack(fill='x', pady=(10, 20))
    image5=customtkinter.CTkFrame(master=scrollable_frame,height=250)
    image5.pack(fill='x', pady=(10, 20))

    image51=customtkinter.CTkFrame(master=scrollable_frame2,height=250)
    image51.pack(fill='x', pady=(10, 20))
    image61=customtkinter.CTkFrame(master=scrollable_frame2,height=250)
    image61.pack(fill='x', pady=(10, 20)) 
    image71=customtkinter.CTkFrame(master=scrollable_frame2,height=250)
    image71.pack(fill='x', pady=(10, 20)) 

    def text_put(pred,porc):
        if pred=='HC':
            text='La imagen no muestra signos de sintomas \n motores asociados a la EP'
        elif pred=='PD':
            text='La imagen muestra caracteristicas \n relacionadas a sintomas motores \n asociados a la EP'
        else:
            text='No existen resultados congruentes para esta imagen'
        return text
    def freq_put(peak,freq):
        if peak>0.05:
            text='El paciente muestra un temblor aproximado \n del '+str(round(freq, 2))+' Hz'
        else:
            text='El paciente no muestra un temblor \n perceptible durante la tarea'
        return text

    label1_title = customtkinter.CTkLabel(image1, text='Tarea 1: Espiral guiada',font=customtkinter.CTkFont(size=15, weight="bold"))
    label1_title.place(relx=0.5)  
    label1_image = customtkinter.CTkLabel(image1, image=img1_result ,text='')
    label1_image.place(relx=0)
    label1_text = customtkinter.CTkLabel(image1,text=text_put(predictions[0],porcentajes[0]),font=customtkinter.CTkFont(size=15, weight="bold"))
    label1_text.place(relx=0.5,rely=0.3)

    label2_title = customtkinter.CTkLabel(image2, text='Tarea 1: Espiral guiada',font=customtkinter.CTkFont(size=15, weight="bold"))
    label2_title.place(relx=0.5)  
    label2_image = customtkinter.CTkLabel(image2, image=img2_result ,text='')
    label2_image.place(relx=0)
    label2_text = customtkinter.CTkLabel(image2,text=text_put(predictions[1],porcentajes[1]),font=customtkinter.CTkFont(size=15, weight="bold"))
    label2_text.place(relx=0.5,rely=0.3)

    label3_title = customtkinter.CTkLabel(image3, text='Tarea 2: Espiral libre',font=customtkinter.CTkFont(size=15, weight="bold"))
    label3_title.place(relx=0.5)  
    label3 = customtkinter.CTkLabel(image3, image=img3_result ,text='')
    label3.place(relx=0)
    label3_text = customtkinter.CTkLabel(image3,text=text_put(predictions[2],porcentajes[2]),font=customtkinter.CTkFont(size=15, weight="bold"))
    label3_text.place(relx=0.5,rely=0.3)

    label4_title = customtkinter.CTkLabel(image5, text='Tarea 3: Meandreo guiado',font=customtkinter.CTkFont(size=15, weight="bold"))
    label4_title.place(relx=0.5)  
    label4 = customtkinter.CTkLabel(image5,image=img4_result ,text='')
    label4.place(relx=0)
    label4_text = customtkinter.CTkLabel(image5,text=text_put(predictions[3],porcentajes[3]),font=customtkinter.CTkFont(size=15, weight="bold"))
    label4_text.place(relx=0.5,rely=0.3)


    label51_title = customtkinter.CTkLabel(image51, text='Tarea 4: Sinusoidal guiada',font=customtkinter.CTkFont(size=15, weight="bold"))
    label51_title.place(relx=0.6)  
    label51 = customtkinter.CTkLabel(image51,image=img5_result ,text='')
    label51.place(relx=0)
    label51_text = customtkinter.CTkLabel(image51,text=freq_put(predictions[4],porcentajes[4]),font=customtkinter.CTkFont(size=15, weight="bold"))
    label51_text.place(relx=0.6,rely=0.3)

    label61_title = customtkinter.CTkLabel(image61, text='Tarea 5: Elevacion de extremidad',font=customtkinter.CTkFont(size=15, weight="bold"))
    label61_title.place(relx=0.6)  
    label61 = customtkinter.CTkLabel(image61,image=img6_result ,text='')
    label61.place(relx=0)
    label61_text = customtkinter.CTkLabel(image61,text=freq_put(predictions[5],porcentajes[5]),font=customtkinter.CTkFont(size=15, weight="bold"))
    label61_text.place(relx=0.6,rely=0.3)

    label71_title = customtkinter.CTkLabel(image71, text='Tarea 5: Reposo de extremidad',font=customtkinter.CTkFont(size=15, weight="bold"))
    label71_title.place(relx=0.6)  
    label71 = customtkinter.CTkLabel(image71,image=img7_result ,text='')
    label71.place(relx=0)
    label71_text = customtkinter.CTkLabel(image71,text=freq_put(predictions[6],porcentajes[6]),font=customtkinter.CTkFont(size=15, weight="bold"))
    label71_text.place(relx=0.6,rely=0.3)

    button_return = customtkinter.CTkButton(master=l13, width=220, text="Pagina principal", command=pagina_principal, corner_radius=6)
    button_return.place(relx=0.9, rely=0.3, anchor=tkinter.CENTER)

    button_return2 = customtkinter.CTkButton(master=l13, width=220, text="Descargar reporte", command=reporte, corner_radius=6)
    button_return2.place(relx=0.9, rely=0.6, anchor=tkinter.CENTER)


def final_screen():
    global r_window
    r_window.destroy()
    app.state(newstate='normal')
    start_frame.pack_forget()
    final_frame.pack()
    frame_final=customtkinter.CTkFrame(master=l12, width=wdth, height=360, corner_radius=15)
    frame_final.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    l_final=customtkinter.CTkLabel(master=l12, text="Gracias por tomar la evaluación",font=('Century Gothic',30))
    l_final.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    #lb2=customtkinter.CTkLabel(master=l5, text="id: "+id,font=('Century Gothic',10))
    #lb2.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)


    #Create custom button
    button_final = customtkinter.CTkButton(master=l12, width=220, text="Resultados", command=resultados, corner_radius=6)
    button_final.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)




def save_data():
    global predictions,porcentajes
    url1 = 'https://parkinsonhdprediction.herokuapp.com/predict'
    url2 = 'https://parkinsonhdprediction.herokuapp.com/freq'

    files={'file': open('out_images/spiral_img.jpg','rb')}
    server=requests.post(url1,files=files)
    diccionario = server.json()
    valor1 = diccionario['class']
    valor2 = diccionario['porcentaje']
    predictions[0]=valor1
    porcentajes[0]=valor2

    files={'file': open('out_images/spiral_trace.jpg','rb')}
    server=requests.post(url1,files=files)
    diccionario = server.json()
    valor1 = diccionario['class']
    valor2 = diccionario['porcentaje']
    predictions[1]=valor1
    porcentajes[1]=valor2

    files={'file': open('out_images/spiral2_img.jpg','rb')}
    server=requests.post(url1,files=files)
    diccionario = server.json()
    valor1 = diccionario['class']
    valor2 = diccionario['porcentaje']
    predictions[2]=valor1
    porcentajes[2]=valor2

    files={'file': open('out_images/meander_img.jpg','rb')}
    server=requests.post(url1,files=files)
    diccionario = server.json()
    valor1 = diccionario['class']
    valor2 = diccionario['porcentaje']
    predictions[3]=valor1
    porcentajes[3]=valor2
    print(valor1)
    print(valor2)

    files={'csv': open('out_data/sensor_data_wave.csv','rb')}
    server=requests.post(url2,files=files)
    diccionario = server.json()
    valor1 = diccionario['freq']
    valor2 = diccionario['peak']
    predictions[4]=valor2
    porcentajes[4]=valor1

    files={'csv': open('out_data/sensor_data_point.csv','rb')}
    server=requests.post(url2,files=files)
    diccionario = server.json()
    valor1 = diccionario['freq']
    valor2 = diccionario['peak']
    predictions[5]=valor2
    porcentajes[5]=valor1

    files={'csv': open('out_data/sensor_data_reposo.csv','rb')}
    server=requests.post(url2,files=files)
    diccionario = server.json()
    valor1 = diccionario['freq']
    valor2 = diccionario['peak']
    predictions[6]=valor2
    porcentajes[6]=valor1

    final_screen()



def point_done2():
    global r_window, l6_r
    l6_r.pack_forget()
    buttonp1 = customtkinter.CTkButton(master=r_window, width=220, text="Terminar", command= save_data,corner_radius=6)
    buttonp1.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

def process_page3():
    global index_aux,ser
    ser.close()
    index_aux=0 
    l1 = []
    with open(r'out_data/data.txt', 'r') as fp:
        l1 = fp.readlines()
    with open(r'out_data/data.txt', 'w') as fp:
        for number, line in enumerate(l1):
            if number not in [0,1,2,4,5,6,7,8,9,10,11,12,13,14,15,-1,-2,-3,-1,-5,-6,-7,-8,-9,-10]:
                fp.write(line)
    #leer nuevos datos 
    df = pd.read_csv('out_data/data.txt', sep=',', header=None,skiprows=1,names=header_names) 
    df.to_csv('out_data/sensor_data_reposo.csv',index=False)
    axis_images('out_data/sensor_data_reposo.csv','reposo')
    point_done2()

def reposo_window():
    global r_window, p_window, counter, state, l6_r
    p_window.destroy()
    r_window = Toplevel(app)
    r_window.geometry("%dx%d"%(wdth,hgt))
    r_window.configure(bg='white')
    l6_r=customtkinter.CTkLabel(master=r_window,fg_color="white",text_color='black')
    l6_r.place(relx=0.5,rely=0.2,anchor=tkinter.CENTER)
    l7=customtkinter.CTkLabel(master=r_window, text='Manten la extremidad evaluada en reposo',text_color='black',font=('Century Gothic',30))
    l7.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)
    counter=4
    state=True
    def count():
        global counter,index_aux, ser, state
        if counter==1 and state:
            counter=16
            state=False
            l8=customtkinter.CTkLabel(master=r_window, text='INICIAR',text_color='firebrick4',font=('Century Gothic',40))
            l8.place(relx=0.5,rely=0.1,anchor=tkinter.CENTER)
        if counter==10:
            ser= serial.Serial('/dev/ttyUSB0',115200,timeout=1)
            ser.flush()
            index_aux=1
        if counter==0:
            process_page3()
            return
        counter=counter-1
        l6_r.configure(text=str(counter), width=wdth, height=105,corner_radius=8, font=('Century Gothic',30))
        l6_r.after(1000,count)
    count()


def point_done():
    global p_window, l6
    l6.pack_forget()
    buttonp1 = customtkinter.CTkButton(master=p_window, width=220, text="Terminar", command= reposo_window,corner_radius=6)
    buttonp1.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

def process_page2():
    global index_aux,ser
    ser.close()
    index_aux=0 
    l1 = []
    with open(r'out_data/data.txt', 'r') as fp:
        l1 = fp.readlines()
    with open(r'out_data/data.txt', 'w') as fp:
        for number, line in enumerate(l1):
            if number not in [0,1,2,4,5,6,7,8,9,10,11,12,13,14,15,-1,-2,-3,-1,-5,-6,-7,-8,-9,-10]:
                fp.write(line)
    #leer nuevos datos 
    df = pd.read_csv('out_data/data.txt', sep=',', header=None,skiprows=1,names=header_names) 
    df.to_csv('out_data/sensor_data_point.csv',index=False)
    axis_images('out_data/sensor_data_point.csv','point')
    os.remove("out_data/data.txt")
    point_done()

def point_window():
    global c_window, p_window, l6
    c_window.destroy() 
    p_window = Toplevel(app)
    p_window.geometry("%dx%d"%(wdth,hgt))
    p_window.configure(bg='white')
    l6=customtkinter.CTkLabel(master=p_window,fg_color="white",text_color='black')
    l6.place(relx=0.5,rely=0.2,anchor=tkinter.CENTER)
    l7=customtkinter.CTkLabel(master=p_window, text='Manten la extremidad evaluada compleamente extendida',text_color='black',font=('Century Gothic',30))
    l7.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)
    def count():
        global counter,index_aux, ser, state
        if counter==1 and state:
            counter=16
            state=False
            l8=customtkinter.CTkLabel(master=p_window, text='INICIAR',text_color='firebrick4',font=('Century Gothic',40))
            l8.place(relx=0.5,rely=0.1,anchor=tkinter.CENTER)
        if counter==10:
            ser= serial.Serial('/dev/ttyUSB0',115200,timeout=1)
            ser.flush()
            index_aux=1
        if counter==0:
            process_page2()
            return
        counter=counter-1
        l6.configure(text=str(counter), width=wdth, height=105,corner_radius=8, font=('Century Gothic',30))
        l6.after(1000,count)
    count()
def process_page1():
    global index_aux,ser
    ser.close()
    index_aux=0 
    l1 = []
    with open(r'out_data/data.txt', 'r') as fp:
        l1 = fp.readlines()
    with open(r'out_data/data.txt', 'w') as fp:
        for number, line in enumerate(l1):
            if number not in [0,1,2,4,5,6,7,8,9,10,11,12,13,14,15,-1,-2,-3,-1,-5,-6,-7,-8,-9,-10]:
                fp.write(line)
    #leer nuevos datos 
    df = pd.read_csv('out_data/data.txt', sep=',', header=None,skiprows=1,names=header_names) 
    df.to_csv('out_data/sensor_data_wave.csv',index=False)
    os.remove("out_data/data.txt")
    axis_images('out_data/sensor_data_wave.csv','wave')
    point_window()

def circle_window():
    global second_window, draw, cvs, mousePressed, last, index_aux, c_window, ser, imgm
    with mss.mss() as sct:
        monitor = {"top": 65, "left": 260, "width": 500, "height":500}
        output = "out_images/meander_img.jpg".format(**monitor)
        # Grab the data
        sct_img = sct.grab(monitor)
        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
    second_window.destroy()
    cvs.destroy()
    mousePressed = False
    last=None
    draw=draw2
    c_window = Toplevel(app)
    c_window.geometry("%dx%d"%(wdth,hgt))
    c_window.configure(bg='white')
    cvs = Canvas(c_window, width=960,height=229,bg='white')
    cvs.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)
    cvs.create_image(0,0, anchor="nw",image=bg3)
    cvs.bind_all('<ButtonPress-1>', press)
    cvs.bind_all('<ButtonRelease-1>', release)
    cvs.bind_all('<Motion>', move)
    button_circle = customtkinter.CTkButton(master=c_window,text='SIGUIENTE',command=process_page1)
    button_circle.place(relx=0.5,rely=0.9,anchor=tkinter.S)
    ser= serial.Serial('/dev/ttyUSB0',115200,timeout=1)
    ser.flush()
    index_aux=1

def meander_window(state):
    global s2_window, draw, cvs, second_window, mousePressed, last, imgm
    app.withdraw()
    if state == False:
        draw=draw1
    mousePressed = False
    last=None
    draw=draw1
    if state:
        second_window.destroy()
        cvs.destroy()
        imgm = Image.new('RGB',(500,500),(255,255,255))
        draw_new = ImageDraw.Draw(imgm)
        draw=draw_new
    second_window = Toplevel(app)
    second_window.geometry("%dx%d"%(wdth,hgt))
    second_window.configure(bg='white')
    cvs = Canvas(second_window, width=500,height=500,bg='white')
    cvs.pack()
    cvs.create_image(0,0, anchor="nw",image=bg2)
    cvs.bind_all('<ButtonPress-1>', press)
    cvs.bind_all('<ButtonRelease-1>', release)
    cvs.bind_all('<Motion>', move)
    button_meander_practica = customtkinter.CTkButton(master=second_window,text='REPETIR',width=200,height=50,command=lambda: meander_window(True))
    button_meander_practica.place(relx=0.1,rely=0.3,anchor=tkinter.S)
    button_meander_done = customtkinter.CTkButton(master=second_window,text='SIGUIENTE',fg_color='Coral',width=200,height=50,command=circle_window)
    button_meander_done.place(relx=0.1,rely=0.6,anchor=tkinter.S)
def meander_tutorial():
    #bienvenido_frame.pack_forget()
    imgs2.save('out_images/spiral2_trace.jpg')
    with mss.mss() as sct:
        monitor = {"top": 65, "left": 260, "width": 500, "height":500}
        output = "out_images/spiral2_img.jpg".format(**monitor)
        # Grab the data
        sct_img = sct.grab(monitor)
        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
    s2_window.destroy()
    app.state(newstate='normal')
    spiral2_tutorial_frame.pack_forget()
    meander_tutorial_frame.pack(fill="both", expand=True)
    img1_result = customtkinter.CTkImage(Image.open("templates/meander_img.jpg"), size=(500,500))
    l_st=customtkinter.CTkLabel(master=meander_tutorial_frame,image=img1_result,text='')
    l_st_text=customtkinter.CTkLabel(master=meander_tutorial_frame,text='TAREA #3',font=('Century Gothic',30),width=20)
    l_st_text.place(relx=0.15,rely=0.2)
    l_st.pack(side='right',padx=20)
    l_st_text1=customtkinter.CTkLabel(master=meander_tutorial_frame,text='Dibuja un meandro siguiendo el patron',font=('Century Gothic',20),width=20)
    l_st_text1.place(relx=0.05,rely=0.4)
    l_st_text2=customtkinter.CTkLabel(master=meander_tutorial_frame,text='- Realiza la tarea de manera fluida',font=('Century Gothic',20),width=20,text_color='dark sea green')
    l_st_text2.place(relx=0.07,rely=0.5)
    l_st_text3=customtkinter.CTkLabel(master=meander_tutorial_frame,text='- No inclines demasiado el boligrafo',font=('Century Gothic',20),width=20,text_color='dark sea green')
    l_st_text3.place(relx=0.07,rely=0.6)
    l_st_text4=customtkinter.CTkLabel(master=meander_tutorial_frame,text='- Evita el contacto con la piel',font=('Century Gothic',20),width=20,text_color='dark sea green')
    l_st_text4.place(relx=0.07,rely=0.7)
    button_st = customtkinter.CTkButton(master=meander_tutorial_frame, width=220, text="Empezar", command=lambda: meander_window(False), corner_radius=6)
    button_st.place(relx=0.25, rely=0.9, anchor=tkinter.CENTER)

def sinusoidal_window(state):
    global draw,canvas,s2_window, imgs2
    app.withdraw()
    if state == False:
            draw=draw3
    if state:
        s2_window.destroy()
        imgs2 = Image.new('RGB',(750,300),(255,255,255))
        draw_new = ImageDraw.Draw(imgs2)
        draw=draw_new
    s2_window = Toplevel(app)
    s2_window.geometry("%dx%d"%(wdth,hgt))
    s2_window.configure(bg='white')
    canvas = Canvas(s2_window, width=750,height=300,bg='white')
    canvas.place(relx=0.2)
    canvas.create_image(0,0, anchor="nw")
    canvas.bind("<Button-1>", start_drawing)
    canvas.bind("<B1-Motion>", continue_drawing)
    canvas.bind("<ButtonRelease-1>", stop_drawing)
    button_spiral_practica = customtkinter.CTkButton(master=s2_window,text='REPETIR',width=200,height=50,command=lambda: spiral_window2(True))
    button_spiral_practica.place(relx=0.1,rely=0.3,anchor=tkinter.S)
    button_spiral_done = customtkinter.CTkButton(master=s2_window,text='SIGUIENTE',fg_color='Coral',width=200,height=50,command=meander_tutorial)
    button_spiral_done.place(relx=0.1,rely=0.6,anchor=tkinter.S)

def spiral_window2(state):
    global draw,canvas,s2_window, imgs2
    app.withdraw()
    if state == False:
            draw=draw3
    if state:
        s2_window.destroy()
        imgs2 = Image.new('RGB',(500,500),(255,255,255))
        draw_new = ImageDraw.Draw(imgs2)
        draw=draw_new
    s2_window = Toplevel(app)
    s2_window.geometry("%dx%d"%(wdth,hgt))
    s2_window.configure(bg='white')
    canvas = Canvas(s2_window, width=500,height=500,bg='white')
    canvas.pack()
    canvas.create_image(0,0, anchor="nw")
    canvas.bind("<Button-1>", start_drawing)
    canvas.bind("<B1-Motion>", continue_drawing)
    canvas.bind("<ButtonRelease-1>", stop_drawing)
    button_spiral_practica = customtkinter.CTkButton(master=s2_window,text='REPETIR',width=200,height=50,command=lambda: spiral_window2(True))
    button_spiral_practica.place(relx=0.1,rely=0.3,anchor=tkinter.S)
    button_spiral_done = customtkinter.CTkButton(master=s2_window,text='SIGUIENTE',fg_color='Coral',width=200,height=50,command=meander_tutorial)
    button_spiral_done.place(relx=0.1,rely=0.6,anchor=tkinter.S)

def spiral2_tutorial():
    global imgs2
    imgs.save('out_images/spiral_trace.jpg')
    with mss.mss() as sct:
        monitor = {"top": 65, "left": 260,"width":500,"height":500}
        output = "out_images/spiral_img.jpg".format(**monitor)
        # Grab the data
        sct_img = sct.grab(monitor)
        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
    #bienvenido_frame.pack_forget()
    newWindow.destroy()
    app.state(newstate='normal')
    spiral_tutorial_frame.pack_forget()
    spiral2_tutorial_frame.pack(fill="both", expand=True)
    img1_result = customtkinter.CTkImage(Image.open("out_images/spiral2_trace.jpg"), size=(500,500))
    l_st=customtkinter.CTkLabel(master=spiral2_tutorial_frame,image=img1_result,text='')
    l_st_text=customtkinter.CTkLabel(master=spiral2_tutorial_frame,text='TAREA #2',font=('Century Gothic',30),width=20)
    l_st_text.place(relx=0.15,rely=0.2)
    l_st.pack(side='right',padx=20)
    l_st_text1=customtkinter.CTkLabel(master=spiral2_tutorial_frame,text='Dibuja una espiral libre',font=('Century Gothic',20),width=20)
    l_st_text1.place(relx=0.05,rely=0.4)
    l_st_text2=customtkinter.CTkLabel(master=spiral2_tutorial_frame,text='- Realiza la tarea de manera fluida',font=('Century Gothic',20),width=20,text_color='dark sea green')
    l_st_text2.place(relx=0.07,rely=0.5)
    l_st_text5=customtkinter.CTkLabel(master=spiral2_tutorial_frame,text='- Realiza la espiral ampliamente',font=('Century Gothic',20),width=20,text_color='dark sea green')
    l_st_text5.place(relx=0.07,rely=0.6)
    l_st_text3=customtkinter.CTkLabel(master=spiral2_tutorial_frame,text='- No inclines demasiado el boligrafo',font=('Century Gothic',20),width=20,text_color='dark sea green')
    l_st_text3.place(relx=0.07,rely=0.7)
    l_st_text4=customtkinter.CTkLabel(master=spiral2_tutorial_frame,text='- Evita el contacto con la piel',font=('Century Gothic',20),width=20,text_color='dark sea green')
    l_st_text4.place(relx=0.07,rely=0.8)
    button_st = customtkinter.CTkButton(master=spiral2_tutorial_frame, width=220, text="Empezar", command=lambda: spiral_window2(False), corner_radius=6)
    button_st.place(relx=0.25, rely=0.9, anchor=tkinter.CENTER)

def spiral_window(state):
    global draw,canvas,newWindow, imgs
    app.withdraw()
    if state:
        newWindow.destroy()
        imgs = Image.new('RGB',(500,500),(255,255,255))
        draw_new = ImageDraw.Draw(imgs)
        draw=draw_new
    newWindow = Toplevel(app)
    newWindow.geometry("%dx%d"%(wdth,hgt))
    newWindow.configure(bg='white')
    canvas = Canvas(newWindow, width=500,height=500,bg='white')
    canvas.pack()
    canvas.create_image(0,0, anchor="nw",image=bg1)
    canvas.bind("<Button-1>", start_drawing)
    canvas.bind("<B1-Motion>", continue_drawing)
    canvas.bind("<ButtonRelease-1>", stop_drawing)
    button_spiral_practica = customtkinter.CTkButton(master=newWindow,text='REPETIR',width=200,height=50,command=lambda: spiral_window(True))
    button_spiral_practica.place(relx=0.1,rely=0.3,anchor=tkinter.S)
    button_spiral_done = customtkinter.CTkButton(master=newWindow,text='SIGUIENTE',fg_color='Coral',width=200,height=50,command=spiral2_tutorial)
    button_spiral_done.place(relx=0.1,rely=0.6,anchor=tkinter.S)

def spiral_tutorial():
    #bienvenido_frame.pack_forget()
    start_frame.pack_forget()
    spiral_tutorial_frame.pack(fill="both", expand=True)
    img1_result = customtkinter.CTkImage(Image.open("out_images/spiral2_trace.jpg"), size=(500,500))
    l_st=customtkinter.CTkLabel(master=spiral_tutorial_frame,image=img1_result,text='')
    l_st_text=customtkinter.CTkLabel(master=spiral_tutorial_frame,text='TAREA #1',font=('Century Gothic',30),width=20)
    l_st_text.place(relx=0.15,rely=0.2)
    l_st.pack(side='right',padx=20)
    l_st_text1=customtkinter.CTkLabel(master=spiral_tutorial_frame,text='Dibuja una espiral siguiendo el patron',font=('Century Gothic',20),width=20)
    l_st_text1.place(relx=0.05,rely=0.4)
    l_st_text2=customtkinter.CTkLabel(master=spiral_tutorial_frame,text='- Realiza la tarea de manera fluida',font=('Century Gothic',20),width=20,text_color='dark sea green')
    l_st_text2.place(relx=0.07,rely=0.5)
    l_st_text3=customtkinter.CTkLabel(master=spiral_tutorial_frame,text='- No inclines demasiado el boligrafo',font=('Century Gothic',20),width=20,text_color='dark sea green')
    l_st_text3.place(relx=0.07,rely=0.6)
    l_st_text4=customtkinter.CTkLabel(master=spiral_tutorial_frame,text='- Evita el contacto con la piel',font=('Century Gothic',20),width=20,text_color='dark sea green')
    l_st_text4.place(relx=0.07,rely=0.7)
    button_st = customtkinter.CTkButton(master=spiral_tutorial_frame, width=220, text="Empezar", command=lambda: spiral_window(False), corner_radius=6)
    button_st.place(relx=0.25, rely=0.9, anchor=tkinter.CENTER)

def bienvenido():
    registrar_next_frame.pack_forget()
    bienvenido_frame.pack()
    app.state(newstate='withdraw')
    app.state(newstate='normal')
    frameb=customtkinter.CTkFrame(master=l5, width=wdth, height=360, corner_radius=15)
    frameb.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    lb1=customtkinter.CTkLabel(master=l5, text="Bienvenid@ "+name_var.get(),font=('Century Gothic',30))
    lb1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    #lb2=customtkinter.CTkLabel(master=l5, text="id: "+id,font=('Century Gothic',10))
    #lb2.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)


    #Create custom button
    buttonb1 = customtkinter.CTkButton(master=l5, width=220, text="Iniciar tutorial", command=lambda: spiral_window(False), corner_radius=6)
    buttonb1.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)
    

def next_registrar():
    global fecha_var
    fecha_var = customtkinter.StringVar()
    registrar_frame.pack_forget()
    registrar_next_frame.pack()
    app.state(newstate='withdraw')
    app.state(newstate='normal')

    #creating custom frame
    framenr=customtkinter.CTkFrame(master=l4, width=320, height=360, corner_radius=15)
    framenr.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    lnr1=customtkinter.CTkLabel(master=framenr, text="Registrarse",font=('Century Gothic',20))
    lnr1.place(x=100, y=45)

    lnr2=customtkinter.CTkLabel(master=framenr, text='Fecha de nacimiento (dd/mm/aaaa)',font=('Century Gothic',10))
    lnr2.place(x=50, y=80)
    entrynr1=customtkinter.CTkEntry(master=framenr, width=220, textvariable=fecha_var)
    entrynr1.place(x=50, y=110)

    c1 = customtkinter.CTkCheckBox(master=framenr, text="Mujer",  onvalue="on", offvalue="off")
    c1.place(x=70, y=170)
    c2 = customtkinter.CTkCheckBox(master=framenr, text="Hombre",  onvalue="on", offvalue="off")
    c2.place(x=170, y=170)
    
    buttonr1 = customtkinter.CTkButton(master=framenr, width=220, text="Registrarse", command=reporte, corner_radius=6)
    buttonr1.place(x=50, y=275)



def registrar():
    global name_var, ape_var, ci_var, framer
    start_frame.pack_forget()
    registrar_frame.pack()
    app.state(newstate='withdraw')
    app.state(newstate='normal')
    name_var = customtkinter.StringVar()
    ape_var = customtkinter.StringVar()
    ci_var = customtkinter.StringVar()
    #creating custom frame
    framer=customtkinter.CTkFrame(master=l3, width=320, height=360, corner_radius=15)
    framer.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    lr1=customtkinter.CTkLabel(master=framer, text="Registrarse",font=('Century Gothic',20))
    lr1.place(x=100, y=45)

    lr2=customtkinter.CTkLabel(master=framer, text="Nombre completo",font=('Century Gothic',10))
    lr2.place(x=50, y=80)
    entryr1=customtkinter.CTkEntry(master=framer,width=220,textvariable=name_var)
    entryr1.place(x=50, y=110)

    lr3=customtkinter.CTkLabel(master=framer, text="Apellido completo",font=('Century Gothic',10))
    lr3.place(x=50, y=145)
    entryr2=customtkinter.CTkEntry(master=framer, width=220, textvariable=ape_var)
    entryr2.place(x=50, y=175)

    lr4=customtkinter.CTkLabel(master=framer, text="Documento de identidad",font=('Century Gothic',10))
    lr4.place(x=50, y=210)
    entryr3=customtkinter.CTkEntry(master=framer, width=220, textvariable=ci_var, show="*")
    entryr3.place(x=50, y=240)

    #Create custom button
    buttonr1 = customtkinter.CTkButton(master=framer, width=220, text="Continuar", command=next_registrar, corner_radius=6)
    buttonr1.place(x=50, y=285)

#*****************************************************************MITAD INTERFAZ



frame1=customtkinter.CTkFrame(master=l1, width=1000, height=hgt, corner_radius=15)
frame1.place(relx=0, rely=0.5, anchor=tkinter.CENTER)
ls1=customtkinter.CTkLabel(master=l1, text="Bienvenido",font=('Century Gothic',40))
ls1.place(x=150, y=200)
ls2=customtkinter.CTkLabel(master=l1, text="Ingresa para tomar el examen nuevamente",font=('Century Gothic',10))
ls2.place(x=150, y=300)
button1 = customtkinter.CTkButton(master=l1, width=220, height=40, text="Ingresar", command=spiral_tutorial,corner_radius=6)
#button1 = customtkinter.CTkButton(master=l1, width=220, height=40, text="Ingresar", command=lambda: spiral_window(False),corner_radius=6)
button1.place(x=150, y=350)
ls3=customtkinter.CTkLabel(master=l1, text="Resgistrate si es tu primera vez",font=('Century Gothic',10))
ls3.place(x=180, y=410)
button2 = customtkinter.CTkButton(master=l1, width=220, height=40, text="Registrarse", command=registrar, corner_radius=6)
button2.place(x=150, y=450)



def checkSerial():
    f   = open("out_data/data.txt", "a")
    if ser.in_waiting>0:
        line=ser.readline().decode(errors='ignore').rstrip()
        print(line)
        f.write(line+'\n')
        f.close()
        f = open('out_data/data.txt','a')

while True:
    app.update()
    app1.update()
    if index_aux==1:
        checkSerial()