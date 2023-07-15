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
    resetpw_window.destroy()
    import login_page

def clear():
    email_entry.delete(0,END)
    password_entry.delete(0,END)
    password2_entry.delete(0,END)

#database
def connectDB():
    try:
        global con
        con=pymysql.connect(host='localhost',user='root',password='password', database='database_name')
        global mycursor
        mycursor=con.cursor()
    except:
        messagebox.showerror('Error','Database connectivity error. Try again.')
        return
def disconnectDB():
    con.commit()
    mycursor.close()
    con.close()

def connect_database():
    if email_entry.get()=='' or password_entry.get()=='' or password2_entry.get()=='':
        messagebox.showerror('Error','All fields are required')
    elif password_entry.get() != password2_entry.get():
        messagebox.showerror('Error','Password mismatch')
    else:
        connectDB()
        query='select * from user_data where email=%s'
        mycursor.execute(query,(email_entry.get()))
        row=mycursor.fetchone()
        if row==None:
            messagebox.showerror('Error','Invalid email')
        else:
            query='update user_data set password=%s where email=%s'
            mycursor.execute(query,(password_entry.get(),email_entry.get()))
            con.commit()
            con.close()
            messagebox.showinfo('success','Password reset is successful')
            clear()
            login_page()

#signup window
resetpw_window=Tk()
resetpw_window.title('signup')
resetpw_window.geometry('1380x776+0+0')
resetpw_window.configure(bg=sc_color)
resetpw_window.resizable(False,False)

#background image
bg_img = ImageTk.PhotoImage(Image.open(path1))
bg_label=Label(resetpw_window, image =bg_img, bg=sc_color)
bg_label.grid()

#signup frame
reset_frame=Frame(resetpw_window,width=350,height=450, bg=sc_color)
reset_frame.place(x=250,y=150)

#back icon
back=PhotoImage(file=path4)
backbutton=Button(resetpw_window,image=back,height=20,width=20, bd=0,bg=sc_color,activebackground=sc_color,cursor='hand2',command=login_page)
backbutton.place(x=0,y=0)

#heading
heading =Label(reset_frame,text='Reset password',fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',18,'bold'),bd=0)
heading.grid(row=0,column=0,padx=10,pady=10)

#email
email_label=Label(reset_frame,text='Email',font=('Microsoft YaHei UI Light',10,'bold'),bg=sc_color,fg=pr_color)
email_label.grid(row=1,column=0,sticky='w',padx=25,pady=(10,0))
email_entry = Entry(reset_frame,font=('Microsoft YaHei UI Light',10,'bold'),bg=sc_color,fg=pr_color,width=30)
email_entry.grid(row=2,column=0,sticky='w',padx=25)

#password
password_label=Label(reset_frame,text='Password',font=('Microsoft YaHei UI Light',10,'bold'),bg=sc_color,fg=pr_color)
password_label.grid(row=3,column=0,sticky='w',padx=25,pady=(10,0))
password_entry = Entry(reset_frame,font=('Microsoft YaHei UI Light',10,'bold'),bg=sc_color,fg=pr_color,width=30)
password_entry.grid(row=4,column=0,sticky='w',padx=25)

#confirm password
password2_label=Label(reset_frame,text='Confirm Password',font=('Microsoft YaHei UI Light',10,'bold'),bg=sc_color,fg=pr_color)
password2_label.grid(row=5,column=0,sticky='w',padx=25,pady=(10,0))
password2_entry = Entry(reset_frame,font=('Microsoft YaHei UI Light',10,'bold'),bg=sc_color,fg=pr_color,width=30)
password2_entry.grid(row=6,column=0,sticky='w',padx=25)

#submit button
submitButton=Button(reset_frame,text='Submit',font=('Microsoft YaHei UI Light',16,'bold'),bd=0,bg=pr_color,fg=sc_color,activebackground=pr_color,activeforeground=sc_color,width=17,cursor='hand2',command=connect_database)
submitButton.grid(row=7,column=0,pady=10)


resetpw_window.mainloop()
