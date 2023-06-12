from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import pymysql

#
pr_color = '#5D3891'
sc_color = 'white'
tr_color = '#C21010'

#images
path1=r"d:\projectX\assets\background_images\BG2.jpeg"
path2=r"d:\projectX\assets\icons\hidden.png"
path3=r"d:\projectX\assets\icons\eye.png"
path4=r"d:\projectX\assets\icons\return.png"

#
def login_page():
    signup_window.destroy()
    import login_page

def clear():
    email_entry.delete(0,END)
    username_entry.delete(0,END)
    password_entry.delete(0,END)
    check.set(0)
    
#database
def connectDB():
    try:
        global con
        con=pymysql.connect(host='localhost',user='root',password='Surajit@123')
        global mycursor
        mycursor=con.cursor()
    except:
        messagebox.showerror('Error','Database connectivity error. Try again.')
        return
def disconnectDB():
    con.commit()
    mycursor.close()
    con.close()


#
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
        con.close()
        messagebox.showinfo('success','Registration is successful')
        clear()
        signup_window.destroy()
        import login_page

#signup window
signup_window=Tk()
signup_window.title('signup')
signup_window.geometry('1380x776+0+0')
signup_window.configure(bg='#fff')
signup_window.resizable(False,False)

#background image
bg_img = ImageTk.PhotoImage(Image.open(path1))
bg_label=Label(signup_window, image =bg_img, bg=sc_color)
bg_label.grid()

#signup frame
signup_frame=Frame(signup_window,width=450,height=450, bg=sc_color)
signup_frame.place(x=250,y=150)

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
login_button = Button(signup_frame,text='Login',fg=sc_color,bg=pr_color,font=('Open Sans',9,'bold'),activebackground=pr_color,activeforeground=sc_color,cursor='hand2',bd=0,width=10,command=login_page)
login_button.place(x=197,y=408)

signup_window.mainloop()