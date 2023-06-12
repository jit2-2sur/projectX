from tkinter import *
from PIL import Image,ImageTk
import mysql.connector
from tkinter import messagebox
import sys
sys.path.insert(1,"D:\\projectX\\screens")  #D:\projectX\admin

mydb = mysql.connector.connect(host='localhost',user='root',password='Surajit@123',database="softwareProject")


class reg:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1500x800+0+0")
        self.root.title("Registration Page")
        self.img_bg = Image.open("D:\\projectX\\assets\\background_images\\BG2.jpeg")
        self.img_bg=self.img_bg.resize((1400,800),Image.Resampling.LANCZOS)
        self.img = ImageTk.PhotoImage(self.img_bg)
        self.lab1 = Label(self.root,image=self.img)
        self.lab1.place(x=0,y=0,relwidth=1,relheight=1)

        self.frame1 = Frame(self.root,bg="white")
        self.frame1.place(x=200,y=120,width="800",height="450")
        
        self.title_Reg = Label(self.frame1,text="Registration Form",font=("times new roman",40,"bold"),fg="black",bg="white")
        self.title_Reg.place(x=230,y=20)
        
        self.name = Label(self.frame1,text="Name",font=("times new roman",15,"bold"),fg="yellow",bg="blue")
        self.name.place(x=250,y=120)        
        self.textname1 = Entry(self.frame1,font=("times new roman",15,"bold"))
        self.textname1.place(x=370,y=120)
        
        self.name = Label(self.frame1,text="Email Id",font=("times new roman",15,"bold"),fg="yellow",bg="blue")
        self.name.place(x=250,y=170)        
        self.textname2 = Entry(self.frame1,font=("times new roman",15,"bold"))
        self.textname2.place(x=370,y=170)

        self.name = Label(self.frame1,text="Contact No.",font=("times new roman",15,"bold"),fg="yellow",bg="blue")
        self.name.place(x=250,y=240)        
        self.textname3 = Entry(self.frame1,font=("times new roman",15,"bold"))
        self.textname3.place(x=370,y=240)

        self.name = Label(self.frame1,text="Password-",font=("times new roman",15,"bold"),fg="yellow",bg="blue")
        self.name.place(x=250,y=310)        
        self.textname4 = Entry(self.frame1,font=("times new roman",15,"bold"))
        self.textname4.place(x=370,y=310)
        
        self.regButton = Button(self.frame1,text="Register",fg="black",bg="white",activebackground="grey",activeforeground="black",font=("times new roman",30,"bold"),command=self.store)
        self.regButton.place(x=280,y=350)

        


    def store(self):
        a,b,c,d=(self.textname1.get(),self.textname2.get(),self.textname3.get(),self.textname4.get())

        self.cur = mydb.cursor()
        self.s="INSERT INTO register VALUES(%s,%s,%s,%s)"
        self.b1 = (a,b,c,d)
        self.cur.execute(self.s,self.b1)
        mydb.commit()
        messagebox.showinfo("Success","Account Created Successfully")
        self.root.destroy()

        

if __name__=="__main__":
    root = Tk()
    register=reg(root)
    root.mainloop()