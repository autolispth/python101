from tkinter import *
from tkinter import ttk #theme of tk
from tkinter import messagebox
from tkinter import PhotoImage
#########################################
import webbrowser
import csv
import math
import pyautocad
import win32com.client
import subprocess


acad = win32com.client.Dispatch("AutoCAD.Application")
####################################
######################################
GUI = Tk()  #หน้าจอโปรแกรมหลัก
GUI.title('โปรแกรมงานแผ่นคลี่') #ชื่อโปรแกรม
GUI.geometry('600x730') #ขนาดโปรแกรม

###FONT###
FONT1 = ('Ps pimpdeed',16 ,'bold')
FONT2 = ('Courier New',20 ,'bold')
FONT3 = ('Arial', 20, 'bold')
FONT4 = ('Ps pimpdeed',18 ,'bold')
####################################
menubar = Menu(GUI)
GUI.config(menu=menubar)

filemenu = Menu(menubar,tearoff=0)
filemenu.add_command(label='Exit',command=GUI.quit)
menubar.add_cascade(label='File',menu=filemenu)

mathmenu = Menu(menubar,tearoff=0)
mathmenu.add_command(label='การบวก')
mathmenu.add_command(label='การลบ')
mathmenu.add_command(label='การคูณ')
mathmenu.add_command(label='การหาร')

menubar.add_cascade(label='Calculate',menu=mathmenu)

def contact():
    url ='https://www.facebook.com/groups/AutolispTH'
    webbrowser.open(url)

helpmenu = Menu(menubar,tearoff=0)
helpmenu.add_command(label='ติดต่อเรา',command=contact)
menubar.add_cascade(label='Help',menu=helpmenu)
################################################
# TAB

Tab = ttk.Notebook(GUI)

T1 = Frame(Tab)
T2 = Frame(Tab)
T3 = Frame(Tab)
T4 = Frame(Tab)

Tab.pack(fill=BOTH,expand=1)

img_t1 = PhotoImage(file='T1.png')
img_t2 = PhotoImage(file='T2.png')
img_t3 = PhotoImage(file='T3.png')
img_t4 = PhotoImage(file='T4.png')

Tab.add(T1,text='ข้องอ',image=img_t1,compound='left')
Tab.add(T2,text='ท่อกลมลด',image=img_t2,compound='left')
Tab.add(T3,text='เหลิี่ยมลดกลม',image=img_t2,compound='left')
Tab.add(T4,text='Help',image=img_t4,compound='left')

##################PYACAD####################
def degrees_to_radians(degrees):
    return degrees * (math.pi / 180)

def radians_to_degrees(degrees):
    return  (degrees * 180) / math.pi

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

##########LABEL#############
#L1 = Label(GUI,text='โปรแกรมแผ่นคลี่ข้องอ', font=FONT4 , fg='green')
#L1.place(x=200,y=10)

#####################
photo = PhotoImage(file='elbow.png') # สร้างรูปภาพ
L2 = Label(T1,image=photo) # สร้าง Label และใส่รูปภาพ
L2.config(width=300, height=350)
L2.place(x=140,y=10)

##########DIAMETER INPUT#########
L3 = Label(T1,text='DIAMETER (mm.)',font=FONT4 ,fg='green')
L3.place(x=150,y=365)

v_diameter = StringVar()
E1 = ttk.Entry(T1,textvariable = v_diameter, font=FONT4, width=10)
E1.place(x=150,y=410)

##########RAIDAL INPUT#########
L4 = Label(T1,text='RADIAL (mm.)',font=FONT4 ,fg='green')
L4.place(x=300,y=365)

v_radius = StringVar()
E2 = ttk.Entry(T1,textvariable = v_radius, font=FONT4, width=10)
E2.place(x=300,y=410)

from datetime import datetime
from pyautocad import Autocad, APoint



###########CALCULATE###########
def Calculate():
    try:
        #autocad_path = r"C:\Program Files (x86)\AutoCAD 2007\acad.exe"
        #subprocess.call([autocad_path])
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
        pbasR = []
        pcurR = []
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
        ###########Draw Left 1 - 19############################
        def drawpl(): 
              acad = Autocad()
              acad.prompt("Hello, Autocad Drawing Pattern Elbow from Python\n")
              num = 0
              p1 = APoint(0, 0)
              p1t = APoint(0, -3.5)
              for i in bd3:
                    text = acad.model.AddText(str(num), p1t, 2.5)
                    p2 = APoint(p1[0], p1[1] + i)
                    acad.model.AddLine(p1, p2)
                    pbas.append(p1)
                    p1 = APoint(p2[0] + w36, p1[1])
                    p1t = APoint(p2[0] + w36, p1t[1])
                    pcur.append(p2)
                    num = 1 + num
        ###########Draw Right 20 - 36############################
        def drawpr(): 
              acad = Autocad()
              num = 18
              bd3R = list(reversed(bd3))
              p1 = APoint(w36 * 18, 0)
              p1t = APoint(p1[0], -3.5)
              for i in bd3R:
                    text = acad.model.AddText(str(num), p1t, 2.5)
                    p2 = APoint(p1[0], p1[1] + i)
                    acad.model.AddLine(p1, p2)
                    pbasR.append(p1)
                    p1 = APoint(p2[0] + w36, p1[1])
                    p1t = APoint(p2[0] + w36, p1t[1])
                    pcurR.append(p2)
                    num = 1 + num
        ###########Draw Curve Left##############
        def drawcurL():
              acad = Autocad()
              p1 = APoint(0, 0)
              for x in pcur:
                    p2 = APoint(x)
                    acad.model.Addline(p1, p2)
                    p1 = p2
        
        ###########Draw Curve Right#############
        def drawcurR():
              acad = Autocad()
              p1 = APoint(pcurR[0])
              for x in pcurR:
                    p2 = APoint(x)
                    acad.model.Addline(p1, p2)
                    p1 = p2       
        #############Draw Base line Left#############
        def drawbasL():
              acad = Autocad()
              p1 = APoint(0, 0)
              for x in pbas:
                    p2 = APoint(x)
                    acad.model.Addline(p1, p2)
                    p1 = p2

        #############Draw Base line Left#############
        def drawbasR():
              acad = Autocad()
              p1 = APoint(0, 0)
              for x in pbasR:
                    p2 = APoint(x)
                    acad.model.Addline(p1, p2)
                    p1 = p2

              acad.app.ZoomExtents()

        def SaveData():
               t = datetime.now().strftime('%d-%m-%y %H:%M:%S')
               bd4.insert(0, t)
               writecsv(bd4) #บันทึกลง csv

        drawpl()
        drawpr()
        drawcurL()
        drawcurR()
        drawbasL()
        drawbasR()
        SaveData()

        data = readcsv()
        for row in data:
              log_text.insert(END, "\n")
              log_text.insert(END, row)
              log_text.insert(END, "\n")

    except:
           messagebox.showwarning('กรุณากรอกตัวเลข','กรุณากรอกตัวเลขรัศมีวงกลม')
           v_diameter.set('')
           v_radius.set('')
           v_diameter.focus()
           #v_radius.focus()
###########END CALCULATE###########  
FB1 = Frame(T1)#หน้ากระดาน log_text
FB1.place(x=215,y=460)
B2 = ttk.Button(FB1, text='Calculate',command=Calculate)
B2.pack(ipadx=30, ipady=10)

#Check Enter
E2.bind('<Return>',lambda x:E2.focus())
B2.bind('<Return>',Calculate) 
################## แสดง Read CSV ด้านล่าง###############################

FB2 = LabelFrame(T1, text='', font=FONT4 , fg='green')  # ชื่อกรอบรวมด้านล่าง
FB2.place(x=30, y=510)

# Create a Text widget to display log messages
log_text = Text(FB2, font=('Angsana New', 16), height=5, width=70)
log_text.pack(pady=15, padx=15)

# Create a Scrollbar widget and attach it to the Text widget
scrollbar = ttk.Scrollbar(FB2, orient=VERTICAL, command=log_text.yview)
scrollbar.place(x=505, y=15, height=150) #x=position X y=position Y
log_text.config(yscrollcommand=scrollbar.set)
################END LOG TEXT########################

###TAB2###################################################################

img = PhotoImage(file='cone.png')

beam_img = ttk.Label(T2,image=img)
beam_img.pack()

L = ttk.Label(T2,text='กรุณากรอกระยะตามภาพ (mm.)',font=FONT1).pack(pady=10)

FTB = Frame(T2) #FTB = Frame of Table
FTB.pack()

v_cone1 = StringVar() #เก็บค่าinput
v_cone2 = StringVar() #เก็บค่าinput
v_cone3 = StringVar() #เก็บค่าinput

L = ttk.Label(FTB,text='Diameter Min.',font=FONT1).grid(row=0,column=0,pady=10,padx=10)
ET21 = ttk.Entry(FTB,textvariable=v_cone1,font=FONT1) 
ET21.grid(row=0,column=1,pady=10)

L = ttk.Label(FTB,text='Diameter Max.',font=FONT1).grid(row=1,column=0,pady=10,padx=10)
ET22 = ttk.Entry(FTB,textvariable=v_cone2,font=FONT1) 
ET22.grid(row=1,column=1,pady=10)

L = ttk.Label(FTB,text='Height of Cone',font=FONT1).grid(row=2,column=0,pady=10,padx=10)
ET23 = ttk.Entry(FTB,textvariable=v_cone3,font=FONT1) 
ET23.grid(row=2,column=1,pady=10)

from pyautocad import Autocad, APoint


def CalculateCone(event=None):
    try:
        #autocad_path = r"C:\Program Files (x86)\AutoCAD 2007\acad.exe"
        #subprocess.call([autocad_path])

        dn = float(v_cone1.get()) #Diameter Min
        dx = float(v_cone2.get()) #Diameter Max
        he = float(v_cone3.get()) #Height
        pi = 3.14159
        rn = dn / 2
        rx = dx / 2
        rz = rx - rn
        lbn = pi * dn
        lbx = pi * dx
        art = math.atan(he / rz)#tan 
        #print(art)
        ang = radians_to_degrees(art)
        #print(ang)
        rad = degrees_to_radians(ang)
        #print(rad)
        hex = rx * math.tan(rad) #Height max
        #print(hex)
        hen = rn * math.tan(rad) #Height min
        #print(hen)
        rax = hex / math.sin(rad) #Radial dia.x
        print(rax)
        ran = hen / math.sin(rad) #Radial dia.n
        angn = (lbn * 180) / (math.pi * ran)
        print(angn)
        angdn = degrees_to_radians(angn)
        print(angdn)        
        angx = (lbx * 180) / (math.pi * rax)
        print(angx)
        a1 = pi * he / 12
        a2 = dx**2 + dn**2 + dx * dn
        calc =  a1 * a2 / 10000000
        print(calc)
        pc = APoint(0, 0)
        #############Draw Base line Left#############
        def draw_arc(center, radius, start_angle, end_angle):
              acad = Autocad()
              acad.prompt("Hello, Autocad Drawing Pattern Cone from Python\n")
              start_angle = math.radians(start_angle)
              end_angle = math.radians(end_angle)
              arc = acad.model.AddArc(center, radius, start_angle, end_angle)
              return arc
        
        draw_arc(pc, rax, 0, angx)  #arc Dia. max
        draw_arc(pc, ran, 0, angn)  #arc Dia. min

        p1 = APoint(ran, 0)
        p2 = APoint(rax, 0)

        x1 = ran * math.cos(angdn)
        y1 = ran * math.sin(angdn)
        p3 = APoint(x1, y1)

        x2 = rax * math.cos(angdn)
        y2 = rax * math.sin(angdn)
        p4 = APoint(x2, y2)

        def drawline(p1, p2):
              acad = Autocad()
              acad.model.Addline(p1, p2)
              acad.app.ZoomExtents()
       
        drawline(p1, p2)
        drawline(p3, p4)

        text = 'ปริมาตร ({}x{}x{}) ทั้งหมด: {:,.3f} ลบ.ม.'.format(dn,dx,he,calc)
        v_result2.set(text)
    except:
        messagebox.showwarning('กรุณากรอกตัวเลข','กรุณากรอกตัวเลขเท่านั้น')
        v_cone1.set('')
        v_cone2.set('')
        v_cone3.set('')
        ET21.focus()


B2 = Button(T2,text='Drawing Cone',command=CalculateCone)
B2.pack(ipadx=20,ipady=10)


#Check Enter
ET21.bind('<Return>',lambda x:ET22.focus())
ET22.bind('<Return>',lambda x:ET23.focus())
ET23.bind('<Return>',CalculateCone)


v_result2 = StringVar()
v_result2.set('---ปริมาตร---')
R2 = ttk.Label(T2,textvariable=v_result2,font=FONT1,foreground='green')
R2.pack(ipady=20)
############################TAB3########################################
img3 = PhotoImage(file='sq2r.png')

sqr_img = ttk.Label(T3,image=img3)
sqr_img.pack()

#L = ttk.Label(T3,text='กรุณากรอกระยะตามภาพ (mm.)',font=FONT1).pack(pady=10)

FTB3 = Frame(T3) #FTB = Frame of Table
FTB3.pack()

v_sqr1 = StringVar() #diameter
v_sqr2 = StringVar() #width
v_sqr3 = StringVar() #length
v_sqr4 = StringVar() #height

L31 = ttk.Label(FTB3, text='Diameter :', font=FONT1).grid(row=0,column=0,pady=10,padx=10)
ET31 = ttk.Entry(FTB3, textvariable=v_sqr1, font=FONT1) 
ET31.grid(row=0,column=1,pady=10)

L32 = ttk.Label(FTB3, text='Width :', font=FONT1).grid(row=1,column=0,pady=10,padx=10)
ET32 = ttk.Entry(FTB3, textvariable=v_sqr2, font=FONT1) 
ET32.grid(row=1,column=1,pady=10)

L33 = ttk.Label(FTB3,text='Length :',font=FONT1).grid(row=2,column=0,pady=10,padx=10)
ET33 = ttk.Entry(FTB3,textvariable=v_sqr3,font=FONT1) 
ET33.grid(row=2,column=1,pady=10)

L34 = ttk.Label(FTB3,text='Height :',font=FONT1).grid(row=3,column=0,pady=10,padx=10)
ET34 = ttk.Entry(FTB3,textvariable=v_sqr4,font=FONT1) 
ET34.grid(row=3,column=1,pady=10)

import win32com.client
from pyautocad import Autocad, APoint
acad = win32com.client.Dispatch("AutoCAD.Application")

def Calculatesqr():
    try:
        da = float(v_sqr1.get()) #Diameter
        print(da)
        wt = float(v_sqr2.get()) #Width
        print(wt)
        lt = float(v_sqr3.get()) #Length
        print(lt)
        he = float(v_sqr4.get()) #Height
        print(he)
        pi = 3.14159
        ra = da / 2
        w1 = wt / 2
        w2 = w1 - ra
        l1 = lt / 2
        l2 = l1 - ra
        lda = pi * da   #เล้นรอบวง
        print(lda)
        bd = [0.0152, 0.0603, 0.1340, 0.2340, 0.3572, 0.5000, 0.6580, 0.8264, 1.0000]
        bd1 = []
        w36 = float(lda / 36)
        print(w36)
        def mlst():
              for x in bd:
                    bd1.append(x * ra)
        
        mlst()
        print(bd1)        
        bd1.insert(0, 0.0)
        wt1 = []
        def wts ():
              for a in bd1:
                    wt1.append(w2 + a)
                    
        wts()
        print(wt1)        
        lt1 = []
        def lts ():
              for a in bd1:
                    lt1.append(l2 + a)
                    
        lts()
        print(lt1)        
        le1 = []
        def lest ():
              global im
              im = len(lt1) - 1
              for x in wt1:
                    iz = lt1[im]
                    le1.append(math.sqrt(x**2 + iz**2))
                    im = im - 1
                         
        lest()
        print(le1)         
        le2 = []
        def lest2 ():
              for x in le1:
                    le2.append(math.sqrt(x**2 + he**2))
                    
        lest2()
        le2.insert(10, w1)
        print(le2)
        def angal (a, b, c):    #alpha angle
              return math.acos((b**2 + c**2 - a**2) / (2 * b * c))
        
        def angbe (a, b, c):    #beta angle
              return math.acos((a**2 + c**2 - b**2) / (2 * a * c))
        
        lstang = []
        lstangr = []
        ang0 = angal(le2[0], lt, le2[0])
        print(radians_to_degrees(ang0))
        ang1 = angal(le2[0], lt, le2[0])
        print(radians_to_degrees(ang1))
        #lstang.append(ang1)
        ang2 = angal(w36, le2[1], le2[0])
        print(radians_to_degrees(ang2))
        lstang.append(ang2)
        lstangr.append(ang2)
        ang3 = angal(w36, le2[2], le2[1])
        print(radians_to_degrees(ang3))
        lstang.append(ang3)
        lstangr.append(ang3)
        ang4 = angal(w36, le2[3], le2[2])
        print(radians_to_degrees(ang4))
        lstang.append(ang4)
        lstangr.append(ang4)
        ang5 = angal(w36, le2[4], le2[3])
        print(radians_to_degrees(ang5))
        lstang.append(ang5)
        lstangr.append(ang5)
        ang6 = angal(w36, le2[5], le2[4])
        print(radians_to_degrees(ang6))
        lstang.append(ang6)
        lstangr.append(ang6)
        ang7 = angal(w36, le2[6], le2[5])
        print(radians_to_degrees(ang7))
        lstang.append(ang7)
        lstangr.append(ang7)
        ang8 = angal(w36, le2[7], le2[6])
        print(radians_to_degrees(ang8))
        lstang.append(ang8)
        lstangr.append(ang8)
        ang9 = angal(w36, le2[8], le2[7])
        print(radians_to_degrees(ang9))
        lstang.append(ang9)
        lstangr.append(ang9)
        ang10 = angal(w36, le2[9], le2[8])
        print(radians_to_degrees(ang10))
        lstang.append(ang10)
        lstangr.append(ang10)
        ang12 = angal(le2[9], wt, le2[9])
        print(radians_to_degrees(ang12))
        lstang.append(ang12)
        lstangr.append(ang12)

        print(lstang)
        print(lstangr)


        p1 = APoint(0, 0)
        p2 = APoint(lt, 0)      
        x2 = le2[0] * math.cos(ang1)
        y2 = le2[0] * math.sin(ang1)
        p3 = APoint(x2, y2)

        def drawline(p1, p2):
              acad = Autocad()
              acad.model.Addline(p1, p2)
       
        drawline(p1, p2)
        #drawline(p1, p3)
        drawline(p2, p3)
        
        def drawpl():
              acad = Autocad()
              acad.prompt("Hello, Autocad Drawing Pattern Square to Round from Python\n")
              lsta = []
              lstl = []
              i = 0
              p3a = p3
              ang = ang1
              for x in lstang:
                    x3 = le2[i] * math.cos(ang)
                    y3 = le2[i] * math.sin(ang)
                    p4 = APoint(x3, y3)
                    lsta.append(ang)
                    lstl.append(p4)
                    #print(lstc)
                    acad.model.Addline(p1, p4)
                    acad.model.Addline(p3a, p4)
                    p3a = p4
                    i = i + 1
                    ang += x

              print(lsta)
              print(lstl)
              p6 = lstl[9]
              lstang.insert(0, ang1)
              atotal = sum(lstang)
              print(radians_to_degrees(atotal))
              acad = Autocad()
              x4 = le2[10] * math.cos(atotal)
              y4 = le2[10] * math.sin(atotal)
              p5 = APoint(x4, y4)
              acad.model.Addline(p1, p5)
              acad.model.Addline(p5, p6)
                          
        drawpl()
        lstang = []

        def drawpr():
              acad = Autocad()
              acad.prompt("Hello, Autocad Drawing Pattern Square to Round from Python\n")
              lstar = []
              lstr = []
              i = 0
              p4a = p3
              angr = 180 - radians_to_degrees(ang0)
              print(angr)
              angr = degrees_to_radians(angr)
              print(lstangr)
              for a in lstangr:
                    x5 = le2[i] * math.cos(angr)
                    y5 = le2[i] * math.sin(angr)
                    p4r = APoint(x5 + lt, y5)
                    lstar.append(angr)
                    lstr.append(p4r)
                    #print(lstc)
                    acad.model.Addline(p2, p4r)
                    acad.model.Addline(p4a, p4r)
                    p4a = p4r
                    i = i + 1
                    angr -= a
                    print(radians_to_degrees(angr))

              print(lstar)
              print(lstr)
              p6 = lstr[9]
              lstangr0 = lstangr
              lstangr0.insert(0, ang0)
              atotar = sum(lstangr0)
              angtotal = 180 - radians_to_degrees(atotar)
              anglr = degrees_to_radians(angtotal)
              print(radians_to_degrees(anglr))
              acad = Autocad()
              x6 = le2[10] * math.cos(anglr)
              y6 = le2[10] * math.sin(anglr)
              p5r = APoint(x6 + lt, y6)
              acad.model.Addline(p2, p5r)
              acad.model.Addline(p5r, p6)
              acad.app.ZoomExtents()
                          
        drawpr()
            
              

    except:
        messagebox.showwarning('กรุณากรอกตัวเลข','กรุณากรอกตัวเลขเท่านั้น')
        v_sqr1.set('')
        v_sqr2.set('')
        v_sqr3.set('')
        v_sqr4.set('')
        ET31.focus()


B3 = Button(T3,text='Drawing SQ2R',command=Calculatesqr)
B3.pack(ipadx=20,ipady=10)


#Check Enter
ET31.bind('<Return>',lambda x:ET32.focus())
ET32.bind('<Return>',lambda x:ET33.focus())
ET33.bind('<Return>',lambda x:ET34.focus())
ET34.bind('<Return>',Calculatesqr)


#####################TAB4###################################################
FL = Frame(T4)
FL.place(x=250,y=250)

L = ttk.Label(FL,text='ติดต่อสอบถามที่',font=FONT2).pack(pady=10)
L = ttk.Label(FL,text='เพจ : AutolispTH ',font=FONT2).pack(pady=10)



GUI.mainloop()