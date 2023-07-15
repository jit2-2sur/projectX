from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import re
import sys
sys.path.insert(1,"D:\\projectX\\screens")
from AdminPg import AdminPg
from NewRegister import reg
import mysql.connector
mydb = mysql.connector.connect(host='localhost',user='root',password='password',database="softwareProject")



class login:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1550x800+0+0")
        self.root.title("Login Page")
        img = Image.open("D:\\projectX\\assets\\background_images\\BG2.jpeg")
        img = img.resize((1400,800),Image.Resampling.LANCZOS)
        self.image_bg = ImageTk.PhotoImage(img)
        self.label_bg_image=Label(root,image=self.image_bg)
        self.label_bg_image.place(x=0,y=0,relwidth=1,relheight=1)

        self.heading = Label(text="MULTIPLEX MANAGEMENT SYSTEM",font=("times new roman",20,"bold"))
        self.heading.place(x=400,y=30)
        
        frame_bg = Frame(self.root,bg="grey")
        frame_bg.place(x=500,y=120,width="350",height="450")

        #Login Icon
        img1 = Image.open("D:\\projectX\\assets\\icons\\login_user_icon.jpg")
        #resizing Image
        img1=img1.resize((80,80),Image.Resampling.LANCZOS)
        self.frame_bg_img = ImageTk.PhotoImage(img1)
        label_frame_bg_img = Label(frame_bg,image=self.frame_bg_img)
        label_frame_bg_img.pack()

        msg = Label(frame_bg,text="Admin Login",font=("times new roman",15,"bold"),bg="red")
        msg.place(x=120,y=100)

        #username
        label_frame_username = Label(frame_bg,text="User email_id",bg="white",font=("times new roman",20,"bold"))
        label_frame_username.place(x=120,y=142)
        self.label_frame_textbox1 = Entry(frame_bg,font=("times new roman",15,"bold"))
        self.label_frame_textbox1.place(x=80,y=190,width=170)
        #User Login_icon Image
        img2 = Image.open("D:\\projectX\\assets\\icons\\user_icon.png")
        #resizing Image
        img2=img2.resize((35,35),Image.Resampling.LANCZOS)
        self.frame_bg_img2 = ImageTk.PhotoImage(img2)
        label_frame_bg_img2 = Label(frame_bg,image=self.frame_bg_img2,bg="red")
        label_frame_bg_img2.place(x=80,y=140)

        #password
        label_frame_password = Label(frame_bg,text="Password",bg="white",font=("times new roman",20,"bold"))
        label_frame_password.place(x=120,y=242)
        self.label_frame_textbox2 = Entry(frame_bg,font=("times new roman",15,"bold"))
        self.label_frame_textbox2.place(x=80,y=290,width=170)
        #User Login_icon Image
        img3 = Image.open("D:\\projectX\\assets\\icons\\login-page-password.png")
        #resizing Image
        img3=img3.resize((35,35),Image.Resampling.LANCZOS)
        self.frame_bg_img3 = ImageTk.PhotoImage(img3)
        label_frame_bg_img3 = Label(frame_bg,image=self.frame_bg_img3,bg="grey")
        label_frame_bg_img3.place(x=80,y=240)
        #button
    
        frame_button=Button(frame_bg,text="Login",bg="white",font=("time new roman",15,"bold"),activeforeground="black",activebackground="grey",command=self.loginid)
        frame_button.place(x=130,y=330)

        reg_button=Button(frame_bg,text="new user? register",bg="white",font=("time new roman",15,"bold"),bd=0,activeforeground="black",activebackground="grey",command=self.register)
        reg_button.place(x=80,y=400)

    def loginid(self):

        a = self.label_frame_textbox1.get()
        b = self.label_frame_textbox2.get()
            
        mycursor = mydb.cursor()
        sql = "SELECT email_id,password FROM register where email_id=%s"

        mycursor.execute(sql,(a,))
        
        try:
            myresult = mycursor.fetchall()
            s1,s2=(myresult[0])
            if self.label_frame_textbox1.get()=="" or self.label_frame_textbox2.get()=="":
                messagebox.showerror("Error","All field are required")
            elif self.label_frame_textbox1.get()==s1 and self.label_frame_textbox2.get()==s2:
                messagebox.showinfo("Success","logged In Successfully")
                self.root.destroy()

                self.window_main=Tk()
                AdminPg(self.window_main)
                self.window_main.mainloop()
                
        except:        
            messagebox.showerror("Invalid","Invalid Username or Password")
            print("Some Invalid Username or password")

    def register(self):
        self.root.destroy()

        self.window_main=Tk()
        reg(self.window_main)
        self.window_main.mainloop()
        
        
       
        
if __name__== "__main__":
    root=Tk()
    app=login(root)
    root.mainloop()
