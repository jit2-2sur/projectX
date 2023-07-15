from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import pymysql

from LoginAdm import login

#colors
pr_color = '#5D3891'
sc_color = 'white'
tr_color = '#C21010'

#images
path1=r"d:\projectX\assets\background_images\BG2.jpeg"
path2=r"d:\projectX\assets\icons\hidden.png"
path3=r"d:\projectX\assets\icons\eye.png"
path4=r"d:\projectX\assets\icons\return.png"

#functions
def connectDB():
    try:
        global con
        con=pymysql.connect(host='localhost',user='root',password='password')
        global mycursor
        mycursor=con.cursor()
        query='use softwareProject'
        mycursor.execute(query)
    except:
        messagebox.showerror('Error','Database connectivity error. Try again.')
        return
def disconnectDB():
    con.commit()
    mycursor.close()
    con.close()

#login functions
def userEnter(event):
    if email.get()=='Email':
        email.delete(0,END)
    if code.get()=='':
        code.insert(0,'Password')
def pwEnter(event):
    if code.get()=='Password':
        code.delete(0,END)
    if email.get()=='':
        email.insert(0,'Email')

def hide():
    openeye.config(file=path2)
    code.config(show='*')
    eyebutton.config(command=show)
def show():
    openeye.config(file=path3)
    code.config(show='')
    eyebutton.config(command=hide)

def clear():
    email.delete(0,END)
    code.delete(0,END)

#redirection
def signup_page():
    login_window.destroy()
    import signup
def resetpw():
    login_window.destroy()
    import resetpw

#login page
def login_user():
    if email.get()=='' or code.get()=='':
        messagebox.showerror('Error','All fields are required')
    else:
        connectDB()
        query='select * from user_data where email=%s and password=%s'
        mycursor.execute(query,(email.get(),code.get()))
        row=mycursor.fetchone()
        if row==None:
            messagebox.showerror('Error','Invalid email or password')
        else:
            query='UPDATE user_data SET active=0'
            mycursor.execute(query)
            con.commit()
            query='UPDATE user_data SET active=1 where email=%s'
            mycursor.execute(query,(email.get()))
            disconnectDB()
            messagebox.showinfo('Welcome','Login is successful')
            clear()
            login_window.destroy()
            import home
        disconnectDB()

def go_admin():
    login_window.destroy()
    window_main=Tk()
    login(window_main)
    window_main.mainloop()

#gui

#login window
login_window=Tk()
login_window.title('login')
login_window.geometry('1380x776+0+0')
login_window.configure(bg='#fff')
login_window.resizable(False,False)

#background image
bg_img = ImageTk.PhotoImage(Image.open(path1))
label=Label(login_window, image =bg_img, bg=sc_color).pack(fill = "both", expand = "yes")

#welcome heading
Label(login_window,text='Welcome',fg=sc_color,bg=tr_color,font=('Microsoft YaHei UI Light',23,'bold')).place(x=340,y=25)
Label(login_window,text='to',fg=sc_color,bg=tr_color,font=('Microsoft YaHei UI Light',23,'bold')).place(x=390,y=65)
Label(login_window,text='Multiplex Ticket Booking System',fg=sc_color,bg=tr_color,font=('Microsoft YaHei UI Light',23,'bold')).place(x=180,y=105)

#login frame
login_frame=Frame(login_window,width=350,height=350, bg=sc_color,bd=10)
login_frame.place(x=250,y=250)

#heading
heading = Label(login_frame,text='sign in',fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',23,'bold'))
heading.place(x=100,y=5)

#email field
email = Entry(login_frame,fg=pr_color,bg=sc_color,bd=0,font=('Microsoft YaHei UI Light',11))
email.place(x=30,y=80)
email.insert(0,'Email')
email.bind('<FocusIn>',userEnter)
Frame(login_frame,width=295,height=2, bg='black').place(x=25,y=107)

#password field
code = Entry(login_frame,fg=pr_color,bg=sc_color,bd=0,font=('Microsoft YaHei UI Light',11))
code.config(show='*')
code.place(x=30,y=150)
code.insert(0,'Password')
code.bind('<FocusIn>',pwEnter)
Frame(login_frame,width=295,height=2, bg='black').place(x=25,y=177)

#eye button for password
openeye=PhotoImage(file=path2)
eyebutton=Button(login_frame,image=openeye,height=20,width=20, bd=0,bg=sc_color,activebackground=sc_color,cursor='hand2',command=show)
eyebutton.place(x=295,y=155)

#forget password
forgetbutton=Button(login_frame,text='Forgot Password?',bd=0,bg=sc_color,activebackground=sc_color,cursor='hand2',activeforeground='black',font=('Microsoft YaHei UI Light',9),command=resetpw)
forgetbutton.place(x=220,y=180)

#login
login_button = Button(login_frame,text='Login',fg=sc_color,bg=pr_color,font=('Open Sans',16,'bold'),activebackground=pr_color,activeforeground=sc_color,cursor='hand2',bd=0,width=20, command=login_user)
login_button.place(x=50,y=230)

#orLabel
#orLabel=Label(login_frame,text='---------Or---------',bg=sc_color,fg=pr_color,font=('Open Sans',12))
#orLabel.place(x=100,y=270)

#other options

#sign up button
signupLabel=Label(login_frame,text='Don\'t have an account!',bg=sc_color,fg=pr_color,font=('Open Sans',12))
signupLabel.place(x=20,y=300)

signup_button = Button(login_frame,text='create new one',fg=pr_color,bg=sc_color,font=('Open Sans',12,'bold'),activebackground=sc_color,activeforeground=sc_color,cursor='hand2',bd=0,command=signup_page)
signup_button.place(x=200,y=298)


admin_button = Button(login_window,text='Admin?',fg=sc_color,bg=pr_color,font=('Open Sans',16,'bold'),activebackground=pr_color,activeforeground=sc_color,cursor='hand2',bd=0,width=20, command=go_admin)
admin_button.place(x=1100,y=10)

login_window.mainloop()
