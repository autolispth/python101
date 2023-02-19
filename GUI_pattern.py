from tkinter import *
from tkinter import ttk #theme of tk
from tkinter import messagebox
from tkinter import PhotoImage

GUI = Tk()  #หน้าจอโปรแกรมหลัก
GUI.title('โปรแกรมบันทึกข้อมูล') #ชื่อโปรแกรม
GUI.geometry('600x750') #ขนาดโปรแกรม

###FONT###
FONT1 = ('impact',20)
FONT2 = ('Courier New',20 ,'bold')
FONT3 = ('Arial', 20, 'bold')

##########LABEL#############
L1 = Label(GUI,text='โปรแกรมแผ่นคลี่ข้องอ', font=FONT2 , fg='green')
L1.place(x=140,y=10)

#####################
photo = PhotoImage(file='elbow.png') # สร้างรูปภาพ
L2 = Label(GUI,image=photo) # สร้าง Label และใส่รูปภาพ
L2.config(width=300, height=350)
L2.place(x=140,y=50)

##########DIAMETER INPUT#########
L3 = Label(GUI,text='DIAMETER (mm.)',font=FONT1 ,fg='green')
L3.place(x=200,y=400)

v_diameter = StringVar()
E1 = ttk.Entry(GUI,textvariable = v_diameter, font=FONT2, width=10)
E1.place(x=200,y=440)

##########RAIDAL INPUT#########
L4 = Label(GUI,text='RADIAL (mm.)',font=FONT1 ,fg='green')
L4.place(x=200,y=480)

v_radius = StringVar()
E2 = ttk.Entry(GUI,textvariable = v_radius, font=FONT2, width=10)
E2.place(x=200,y=520)

###########CALCULATE###########
def Calculate():
	try:
		unit = 'ตร.ม.'
		unit1 = 'มม.'
		radius = float(v_radius.get())
		diameter = float(v_diameter.get())
		pi = 3.14159
		calc = pi * (radius**2) / 1000000
		calc1 = pi * diameter
		text = 'พื้นที่วงกลม = {:,.2f} {}'.format(calc,unit)
		text1 = 'เส้นรอบวง = {:,.2f} {}'.format(calc1,unit1)
		print(text)
		v_result.set(text)
		v_radius.set('')
		v_result1.set(text1)
		v_diameter.set('')
	except:
		messagebox.showwarning('กรุณากรอกตัวเลข','กรุณากรอกตัวเลขรัศมีวงกลม')
		v_radius.set('')
		v_radius.focus()
		v_diameter.set('')
		v_diameter.focus('')

###############
FB1 = Frame(GUI)#หน้ากระดาน
FB1.place(x=200,y=580)
B2 = ttk.Button(FB1,text='Calculate', command=Calculate, )
B2.pack(ipadx=30,ipady=20)

#Check Enter
E1.bind('<Return>',Calculate)

v_result = StringVar()
v_result.set('---ผลลัพธ์---')
R1 = ttk.Label(GUI,textvariable = v_result, font=FONT3, foreground='green')
R1.place(x=130,y=650)

v_result1 = StringVar()
v_result1.set('---ผลลัพธ์---')
R1 = ttk.Label(GUI,textvariable = v_result1, font=FONT3, foreground='green')
R1.place(x=130,y=680)

GUI.mainloop()
