from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import pymysql

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
        con=pymysql.connect(host='localhost',user='root',password='lkjhg')
        global mycursor
        mycursor=con.cursor()
    except:
        messagebox.showerror('Error','Database connectivity error. Try again.')
        return
def disconnectDB():
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
    login_frame.place_forget()
    signup_frame.place(x=250,y=150)
def resetpw():
    root_window.destroy()
    import resetpw

#login page
def login_user():
    if email.get()=='' or code.get()=='':
        messagebox.showerror('Error','All fields are required')
    else:
        connectDB()
        query='use softwareProject'
        mycursor.execute(query)
        query='select * from user_data where email=%s and password=%s'
        mycursor.execute(query,(email.get(),code.get()))
        row=mycursor.fetchone()
        if row==None:
            messagebox.showerror('Error','Invalid email or password')
        else:
            messagebox.showinfo('Welcome','Login is successful')
            clear()
            root_window.destroy()
            import home
        disconnectDB()

#gui

#login window
root_window=Tk()
root_window.title('login')
root_window.geometry('1380x776+0+0')
root_window.configure(bg='#fff')
root_window.resizable(False,False)

#background image
bg_img = ImageTk.PhotoImage(Image.open(path1))
label=Label(root_window, image =bg_img, bg=sc_color).pack(fill = "both", expand = "yes")

#welcome heading
Label(root_window,text='Welcome',fg=sc_color,bg=tr_color,font=('Microsoft YaHei UI Light',23,'bold')).place(x=340,y=25)
Label(root_window,text='to',fg=sc_color,bg=tr_color,font=('Microsoft YaHei UI Light',23,'bold')).place(x=390,y=65)
Label(root_window,text='Multiplex Ticket Booking System',fg=sc_color,bg=tr_color,font=('Microsoft YaHei UI Light',23,'bold')).place(x=180,y=105)

#login frame
login_frame=Frame(root_window,width=350,height=350, bg=sc_color,bd=10)
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




##########################################################################################################
#signup
def clear2():
    email_entry.delete(0,END)
    username_entry.delete(0,END)
    password_entry.delete(0,END)
    check.set(0)
    
#signup main
def connect_database():
    if email_entry.get()=='' or username_entry.get()=='' or password_entry.get()=='' or password2_entry.get()=='':
        messagebox.showerror('Error','All fields are required')
    elif password_entry.get() != password2_entry.get():
        messagebox.showerror('Error','Password mismatch')
    elif check.get()==0:
        messagebox.showerror('Error','Please accept terms & conditions')
    else:
        connectDB()
        try:
            query='create database softwareProject'
            mycursor.execute(query)
            query='use softwareProject'
            mycursor.execute(query)
            query='create table user_data(u_id int auto_increment primary key not null, email varchar(50) unique, username varchar(30), password varchar(20))'
            mycursor.execute(query)
        except:
            mycursor.execute('use softwareProject')

        query='insert into user_data(email,username,password) values(%s,%s,%s)'
        mycursor.execute(query,(email_entry.get(),username_entry.get(),password_entry.get()))
        con.commit()
        disconnectDB()

        messagebox.showinfo('success','Registration is successful')
        clear2()
        root_window.destroy()
        import login_page

#signup frame
signup_frame=Frame(root_window,width=450,height=450, bg=sc_color)

#heading
heading =Label(signup_frame,text='create new account',fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',18,'bold'),bd=0)
heading.grid(row=0,column=0,padx=10,pady=10)

#email
email_label=Label(signup_frame,text='Email',font=('Microsoft YaHei UI Light',10,'bold'),bg=sc_color,fg=pr_color)
email_label.grid(row=1,column=0,sticky='w',padx=25,pady=(10,0))
email_entry = Entry(signup_frame,font=('Microsoft YaHei UI Light',10,'bold'),bg=sc_color,fg=pr_color,width=30)
email_entry.grid(row=2,column=0,sticky='w',padx=25)

#username
user_label=Label(signup_frame,text='Username',font=('Microsoft YaHei UI Light',10,'bold'),bg=sc_color,fg=pr_color)
user_label.grid(row=3,column=0,sticky='w',padx=25,pady=(10,0))
username_entry = Entry(signup_frame,font=('Microsoft YaHei UI Light',10,'bold'),bg=sc_color,fg=pr_color,width=30)
username_entry.grid(row=4,column=0,sticky='w',padx=25)

#password
password_label=Label(signup_frame,text='Password',font=('Microsoft YaHei UI Light',10,'bold'),bg=sc_color,fg=pr_color)
password_label.grid(row=5,column=0,sticky='w',padx=25,pady=(10,0))
password_entry = Entry(signup_frame,font=('Microsoft YaHei UI Light',10,'bold'),bg=sc_color,fg=pr_color,width=30)
password_entry.grid(row=6,column=0,sticky='w',padx=25)

#confirm password
password2_label=Label(signup_frame,text='Confirm Password',font=('Microsoft YaHei UI Light',10,'bold'),bg=sc_color,fg=pr_color)
password2_label.grid(row=7,column=0,sticky='w',padx=25,pady=(10,0))
password2_entry = Entry(signup_frame,font=('Microsoft YaHei UI Light',10,'bold'),bg=sc_color,fg=pr_color,width=30)
password2_entry.grid(row=8,column=0,sticky='w',padx=25)

#agree condition
check = IntVar()
agree=Checkbutton(signup_frame,text='I agree to the Terms & Conditions',font=('Microsoft YaHei UI Light',9,'bold'),bg=sc_color,fg=pr_color,activebackground=sc_color,activeforeground=pr_color,cursor='hand2',variable=check)
agree.grid(row=9,column=0,pady=10,padx=15)

#signup button
signupButton=Button(signup_frame,text='Sign up',font=('Microsoft YaHei UI Light',16,'bold'),bd=0,bg=pr_color,fg=sc_color,activebackground=pr_color,activeforeground=sc_color,width=17,cursor='hand2',command=connect_database)
signupButton.grid(row=10,column=0,pady=10)

#already account
alreadyaccount = Label(signup_frame,text='Already have an acoount?',font=('Microsoft YaHei UI Light',9,'bold'),bg=sc_color,fg=pr_color,activebackground=sc_color,activeforeground=pr_color)
alreadyaccount.grid(row=11,column=0,sticky='w',padx=25,pady=10)

#login
login_button = Button(signup_frame,text='Login',fg=sc_color,bg=pr_color,font=('Open Sans',9,'bold'),activebackground=pr_color,activeforeground=sc_color,cursor='hand2',bd=0,width=10)
login_button.place(x=197,y=408)

root_window.mainloop()
