from tkinter import *
from tkinter import ttk #theme of tk
from tkinter import messagebox
from tkinter import PhotoImage
#########################################
import csv
import math
import pyautocad
import win32com.client

acad = win32com.client.Dispatch("AutoCAD.Application")

##################PYACAD####################
def degrees_to_radians(degrees):
    return degrees * (math.pi / 180)

def writecsv(datalist):
    with open('data-bd1.csv','a',encoding='utf-8',newline='') as file:
        fw = csv.writer(file) #fw = file writer
        fw.writerow(datalist) # datalist = ['pen','pencil','eraser']

def readcsv():
    with open('data-bd1.csv',encoding='utf-8',newline='') as file:
        fr = csv.reader(file) #fr = file reader
        data = list(fr)
    return data

def adddata(text):
    with open('add-bd1.txt','a',encoding= 'utf-8') as file:
        file.writelines(text + '\n')

######################################
GUI = Tk()  #หน้าจอโปรแกรมหลัก
GUI.title('โปรแกรมบันทึกข้อมูล') #ชื่อโปรแกรม
GUI.geometry('600x730') #ขนาดโปรแกรม

###FONT###
FONT1 = ('impact',20)
FONT2 = ('Courier New',20 ,'bold')
FONT3 = ('Arial', 20, 'bold')
FONT4 = ('Ps pimpdeed',20 ,'bold')

##########LABEL#############
L1 = Label(GUI,text='โปรแกรมแผ่นคลี่ข้องอ', font=FONT4 , fg='green')
L1.place(x=200,y=10)

#####################
photo = PhotoImage(file='elbow.png') # สร้างรูปภาพ
L2 = Label(GUI,image=photo) # สร้าง Label และใส่รูปภาพ
L2.config(width=300, height=350)
L2.place(x=140,y=50)

##########DIAMETER INPUT#########
L3 = Label(GUI,text='DIAMETER (mm.)',font=FONT4 ,fg='green')
L3.place(x=100,y=400)

v_diameter = StringVar()
E1 = ttk.Entry(GUI,textvariable = v_diameter, font=FONT2, width=10)
E1.place(x=100,y=440)

##########RAIDAL INPUT#########
L4 = Label(GUI,text='RADIAL (mm.)',font=FONT4 ,fg='green')
L4.place(x=300,y=400)

v_radius = StringVar()
E2 = ttk.Entry(GUI,textvariable = v_radius, font=FONT2, width=10)
E2.place(x=300,y=440)

from datetime import datetime
from pyautocad import Autocad, APoint
###########CALCULATE###########
def Calculate():
    try:
        radius = float(v_radius.get())
        diameter = float(v_diameter.get())
        bd = [0.0152, 0.0603, 0.1340, 0.2340, 0.3572, 0.5000, 0.6580, 0.8264]
        bd1 = []
        bd2 = []
        bd3 = []
        bd4 = []
        bd1r = []
        pcur = []
        pbas = []
        pi = 3.14159
        w36 = pi * diameter / 36
        rd = diameter / 2.0
        rd1 = radius - rd
        rdx = rd * 1.00
        angdg = 11.25
        angrd = degrees_to_radians(angdg) 
        def mlst():
                      
                      for x in bd:
                             bd1.append(x * rd)
                             
        def mlst1():

                      for x in reversed(bd1):
                             bd1r.append(rd + rd - x)
        mlst()
        mlst1()
        bd1.append(rdx)
        bd1.insert(0, 0.0)
        bd1r.append(diameter)
        bd2 = bd1 + bd1r
        def mlst2():
                     for x in bd2:
                           rdx = rd1 + x
                           rdx0 = round(rdx * math.tan(angrd), 3)
                           bd3.append(rdx0)
        mlst2()

        bd4 = bd3
        def drawpl(): 
              acad = Autocad()
              acad.prompt("Hello, Autocad from Python\n")
              p1 = APoint(0, 0)
              for i in bd3:
                    p2 = APoint(p1[0], p1[1] + i)
                    acad.model.AddLine(p1, p2)
                    pbas.append(p1)
                    p1 = APoint(p2[0] + w36, p1[1])
                    pcur.append(p2)

        def drawcur():
              acad = Autocad()
              p1 = APoint(0, 0)
              for x in pcur:
                    p2 = APoint(x)
                    acad.model.Addline(p1, p2)
                    p1 = p2

        def drawbas():
              acad = Autocad()
              p1 = APoint(0, 0)
              for x in pbas:
                    p2 = APoint(x)
                    acad.model.Addline(p1, p2)
                    p1 = p2

        def SaveData():
               t = datetime.now().strftime('%d-%m-%y %H:%M:%S')
               bd4.insert(0, t)
               writecsv(bd4) #บันทึกลง csv
               
        drawpl()
        drawcur()
        drawbas()
        SaveData()
        data = readcsv()
        for row in data:
              log_text.insert(END, "\n")
              log_text.insert(END, row)
              log_text.insert(END, "\n")
        
        drawpl()

  
    except:
           messagebox.showwarning('กรุณากรอกตัวเลข','กรุณากรอกตัวเลขรัศมีวงกลม')
           v_diameter.set('')
           v_radius.set('')
           #v_diameter.focus()
           #v_radius.focus()
        

  
###############
FB1 = Frame(GUI)#หน้ากระดาน
FB1.place(x=215,y=480)
B2 = ttk.Button(FB1, text='Calculate',command=Calculate)
B2.pack(ipadx=30, ipady=10)

####################DRAW ACAD#################



################## แสดง Read CSV ด้านล่าง###############################

FB2 = LabelFrame(GUI, text='', font=FONT4 , fg='green')  # ชื่อกรอบรวมด้านล่าง
FB2.place(x=30, y=530)

# Create a Text widget to display log messages
log_text = Text(FB2, font=('Angsana New', 16), height=5, width=70)
log_text.pack(pady=15, padx=15)

# Create a Scrollbar widget and attach it to the Text widget
scrollbar = ttk.Scrollbar(FB2, orient=VERTICAL, command=log_text.yview)
scrollbar.place(x=505, y=15, height=150) #x=position X y=position Y
log_text.config(yscrollcommand=scrollbar.set)


GUI.mainloop()