from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import pymysql
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


#colors
pr_color = '#5D3891'
sc_color = 'white'
tr_color = '#C21010'
font_size=10

#images
path1=r"d:\projectX\assets\background_images\BG2.jpeg"
path4=r"d:\projectX\assets\icons\return.png"

#global variables
global selected_movie_id
global selected_movie_name
global selected_hall_id
global selected_hall_name
global selected_show_id
global selected_user_id
global selected_user_name
global selected_book_id
global selected_ticket_id
global seat_list

selected_movie_id=0
selected_movie_name='No movie selected'
selected_hall_id=0
selected_hall_name='No cinema hall selected'
selected_show_id=0
selected_user_id=0
selected_user_name='No User'
selected_book_id=0
selected_ticket_id=0
seat_list=[]

#database connections
def connectDB():
    try:
        global con
        con=pymysql.connect(host='localhost',user='root',password='pw',database='softwareProject')
        global mycursor
        mycursor=con.cursor()
    except:
        messagebox.showerror('Error','Database connectivity error. Try again.')
        return
def disconnectDB():
    con.commit()
    mycursor.close()
    con.close()

#userconnect
connectDB()
query='select * from user_data'
mycursor.execute(query)
user_data=mycursor.fetchall()
i=0
for i,user in enumerate(user_data):
    if user[4]==1:
        selected_user_id = user[0]
        selected_user_name=user[2]
        print('user logged in: ',selected_user_id,'and username: ',selected_user_name)
disconnectDB()

#functions
def userEnter(event):
    if search_label.get()=='Search Movie':
        search_label.delete(0,END)

###############################################
def logout_redirect():
    connectDB()
    query='UPDATE user_data SET active=0 where u_id=%s'
    mycursor.execute(query,(selected_user_id))
    disconnectDB()
    home_window.destroy()
    import login_page

def pw_change():
    connectDB()
    query='UPDATE user_data SET active=0 where u_id=%s'
    mycursor.execute(query,(selected_user_id))
    disconnectDB()
    home_window.destroy()
    import resetpw

def show_user_data():
    destroy_dialog_frame()
    global dialog_frame
    dialog_frame = Frame(home_window,width=650,height=350)
    dialog_frame.place(x=50,y=200)
    Label(dialog_frame, text='User Data', font=("Arial", 12)).place(x=250,y=10)

    i=0
    u_list=['user_id : ','user email : ','username : ']
    for i,user in enumerate(user_data):
        print('user : ',user)
        if user[0]==selected_user_id:
            j=0
            for j,value in enumerate(user):
                if j<3:
                    a=40
                    b=60+60*j
                    Label(dialog_frame, text=u_list[j], font=("Arial", 12)).place(x=a,y=b)
                    Label(dialog_frame, text=value, font=("Arial", 12)).place(x=a+200,y=b)

    pw_button = Button(dialog_frame, text="change password", command=pw_change)
    pw_button.place(x=40,y=250)
    logout_button = Button(dialog_frame, text="LogOut", command=logout_redirect)
    logout_button.place(x=250,y=300)
    close_button = Button(dialog_frame, text="Close", command=dialog_frame.destroy)
    close_button.place(x=350,y=300)
#########################################################About_us
def show_aboutus():
    destroy_dialog_frame()
    global dialog_frame
    dialog_frame = Frame(home_window,width=650,height=350)
    dialog_frame.place(x=50,y=200)
    faq_label = Label(dialog_frame, text="this is a movie ticket booking software", font=("Arial", 12))
    faq_label.place(x=10,y=10)

    close_button = Button(dialog_frame, text="Close", command=dialog_frame.destroy)
    close_button.place(x=300,y=300)

########################################################Contacts
def show_contact():
    destroy_dialog_frame()
    global dialog_frame
    dialog_frame = Frame(home_window,width=650,height=350)
    dialog_frame.place(x=50,y=200)
    faq_label = Label(dialog_frame, text="\nName: Surajit Ghorai\n\nPhone: 8159966760\n\nEmail: it.20203013@gmail.com",justify="left", font=("Arial", 12))
    faq_label.place(x=10,y=10)

    close_button = Button(dialog_frame, text="Close", command=dialog_frame.destroy)
    close_button.place(x=300,y=300)

###############################################################Faqs
def show_faq():
    destroy_dialog_frame()
    global dialog_frame
    dialog_frame = Frame(home_window,width=650,height=350)
    dialog_frame.place(x=50,y=200)
    faq_label = Label(dialog_frame, text="Q1. xxx \n\nAns. yyy \n\nQ2. xxx \n\nAns. yyy \n\n", font=("Arial", 12))
    faq_label.place(x=10,y=10)

    close_button = Button(dialog_frame, text="Close", command=dialog_frame.destroy)
    close_button.place(x=300,y=300)

#########################################################home_original
def destroy_dialog_frame():
    global dialog_frame
    if dialog_frame:
        dialog_frame.destroy()

######################################################movie_list
def show_movie_list():
    connectDB() 
    query='select movie_id,movie_name,lang,movie_type from movies'
    mycursor.execute(query)
    movie_lists=mycursor.fetchall()
    if len(movie_lists)==0:
        messagebox.showinfo('Error','No movies Found')
    else:
        def button_clicked(event):
            button = event.widget
            button_data = button_data_dict[button]
            global selected_movie_id
            selected_movie_id=int(button_data['text'])
            global selected_movie_name
            selected_movie_name=button_data['name']
            print("Button clicked - Name:", selected_movie_name,"movie id =" ,selected_movie_id)
            show_movie_details(selected_movie_id)

        destroy_dialog_frame()
        global dialog_frame
        dialog_frame = Frame(home_window,width=650,height=350,bg=sc_color)
        dialog_frame.place(x=50,y=200)

        button_data_dict = {}
        movid=0
        i,j=0,0
        for i, movie in enumerate(movie_lists):
            for j, value in enumerate(movie):
                a=40+40*i
                b=20+200*(j-1)

                bttn_name='button'+str(i)
                if j==0:
                    movid=value
                    continue
                elif j==1:
                    bttn_name = Button(dialog_frame, text=value,name=bttn_name, font=("Arial", 12),bd=0,bg=sc_color)
                    button_data_dict[bttn_name] = {'name': value, 'text': movid}
                    bttn_name.place(x=b,y=a)
                    bttn_name.bind("<Button-1>", button_clicked)
                else:
                    label = Label(dialog_frame, text=value, font=("Arial", 12),bd=0,bg=sc_color)
                    label.place(x=b,y=a)

        close_button = Button(dialog_frame, text="Close", command=dialog_frame.destroy)
        close_button.place(x=300,y=300)

    disconnectDB()

###########################################
def show_hall_list():
    connectDB() 
    query='select * from cinema_hall'
    mycursor.execute(query)
    hall_lists=mycursor.fetchall()
    if len(hall_lists)==0:
        messagebox.showinfo('Error','No movies Found')
    else:
        destroy_dialog_frame()
        global dialog_frame
        dialog_frame = Frame(home_window,width=650,height=350,bg=sc_color)
        dialog_frame.place(x=50,y=200)
        i,j,k=0,0,0
        for i,hall in enumerate(hall_lists):
            a=40+40*i
            k=0
            for j,val in enumerate(hall):
                b=20+200*k
                if j==0 or j==2 or j==4:
                    continue
                else:
                    bttn_name = Label(dialog_frame, text=val, font=("Arial", 12),bd=0,bg=sc_color)
                    bttn_name.place(x=b,y=a)
                    k+=1
        close_button = Button(dialog_frame, text="Close", command=dialog_frame.destroy)
        close_button.place(x=300,y=300)

    disconnectDB()

#######################################
def show_movie_details(m_id):
    connectDB() 
    query='select * from movies where movie_id=%s'
    mycursor.execute(query,(str(m_id)))
    movie_details=mycursor.fetchall()
    if len(movie_details)==0:
        messagebox.showinfo('Error','No movies Found')
    else:
        destroy_dialog_frame()
        global dialog_frame
        dialog_frame = Frame(home_window,width=650,height=350,bg=sc_color)
        dialog_frame.place(x=50,y=150)

        heading_label=Label(dialog_frame,text='Movie Details',fg=tr_color,bg=sc_color,font=('Microsoft YaHei UI Light',23,'bold'),justify='left')
        heading_label.grid(row=0,column=1)

        movie_label=Label(dialog_frame,text='Movie Name : ',fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',18,'bold'))
        movie_label.grid(row=1,column=0,sticky='w',padx=25,pady=(10,10))
        movie_name=Label(dialog_frame,text=movie_details[0][1],fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',18,'bold'))
        movie_name.grid(row=1,column=1,sticky='w',padx=25,pady=(10,10))
        movie_type=Label(dialog_frame,text=movie_details[0][8],fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',18,'bold'))
        movie_type.grid(row=1,column=2,sticky='w',padx=25,pady=(10,10))

        movie_desc=Label(dialog_frame,text='Movie Description : ',fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',18,'bold'))
        movie_desc.grid(row=2,column=0,sticky='w',padx=25,pady=(10,10))
        movie_desc_de=Label(dialog_frame,text=movie_details[0][2],fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',18,'bold'))
        movie_desc_de.grid(row=2,column=1,sticky='w',padx=25,pady=(10,10))

        duration=Label(dialog_frame,text='Duration',fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',18,'bold'))
        duration.grid(row=3,column=0,sticky='w',padx=25,pady=(10,10))
        dur_time=Label(dialog_frame,text=movie_details[0][3],fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',18,'bold'))
        dur_time.grid(row=3,column=1,sticky='w',padx=25,pady=(10,10))

        Lang=Label(dialog_frame,text='Language : ',fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',18,'bold'))
        Lang.grid(row=4,column=0,sticky='w',padx=25,pady=(10,10))
        lang_name=Label(dialog_frame,text=movie_details[0][4],fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',18,'bold'))
        lang_name.grid(row=4,column=1,sticky='w',padx=25,pady=(10,10))

        release=Label(dialog_frame,text='release date : ',fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',18,'bold'))
        release.grid(row=5,column=0,sticky='w',padx=25,pady=(10,10))
        release_date=Label(dialog_frame,text=movie_details[0][5],fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',18,'bold'))
        release_date.grid(row=5,column=1,sticky='w',padx=25,pady=(10,10))

        genre=Label(dialog_frame,text='genre',fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',18,'bold'))
        genre.grid(row=6,column=0,sticky='w',padx=25,pady=(10,10))
        genre_name=Label(dialog_frame,text=movie_details[0][7],fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',18,'bold'))
        genre_name.grid(row=6,column=1,sticky='w',padx=25,pady=(10,10))

        country=Label(dialog_frame,text='country',fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',18,'bold'))
        country.grid(row=7,column=0,sticky='w',padx=25,pady=(10,10))
        country_name=Label(dialog_frame,text=movie_details[0][6],fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',18,'bold'))
        country_name.grid(row=7,column=1,sticky='w',padx=25,pady=(10,10))

        book=Button(dialog_frame,text='book tickets',fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',18,'bold'),command=movie_book)
        book.grid(row=8,column=1,sticky='w',padx=25,pady=(10,10))

    close_button = Button(dialog_frame, text="Go Back", command=go_back)
    close_button.place(x=30,y=10)
    disconnectDB()

def go_back():
    global selected_movie_id
    selected_movie_id=0
    dialog_frame.destroy()

#########################################
def search_movie():
    connectDB()
    query='select movie_id,movie_name,lang,movie_type from movies where movie_name=%s'
    mycursor.execute(query,(search_label.get()))
    movies=mycursor.fetchall()
    if len(movies)==0:
        messagebox.showinfo('Error','the movie is not Found')
    else:
        def button_clicked(event):
            button = event.widget
            button_data = button_data_dict1[button]
            global selected_movie_id
            selected_movie_id=int(button_data['text'])
            global selected_movie_name
            selected_movie_name=button_data['name']
            print("Button clicked - Name:", selected_movie_name,"movie id =" ,selected_movie_id)
            show_movie_details(selected_movie_id)

        destroy_dialog_frame()
        global dialog_frame
        dialog_frame = Frame(home_window,width=650,height=350,bg=sc_color)
        dialog_frame.place(x=50,y=200)

        button_data_dict1 = {}
        i,j=0,0
        for i, movie in enumerate(movies):
            for j, value in enumerate(movie):
                a=40+40*i
                b=20+200*(j-1)

                bttn_name='button'+str(i)
                if j==0:
                    movid=value
                    continue
                elif j==1:
                    bttn_name = Button(dialog_frame, text=value,name=bttn_name, font=("Arial", 12),bd=0,bg=sc_color)
                    button_data_dict1[bttn_name] = {'name': value, 'text': movid}
                    bttn_name.place(x=b,y=a)
                    bttn_name.bind("<Button-1>", button_clicked)
                else:
                    label = Label(dialog_frame, text=value, font=("Arial", 12),bd=0,bg=sc_color)
                    label.place(x=b,y=a)

        close_button = Button(dialog_frame, text="Close", command=dialog_frame.destroy)
        close_button.place(x=300,y=300)
    con.close()

#############################################################################################
def movie_book(): 
    global selected_movie_id
    global selected_hall_id
    global selected_show_id
    if selected_movie_id==0:
        print(selected_movie_id,selected_hall_id,selected_show_id)
        show_movie_list()
    elif selected_hall_id==0:
        print(selected_movie_id,selected_hall_id,selected_show_id)
        select_hall()
    elif selected_show_id==0:
        print(selected_movie_id,selected_hall_id,selected_show_id)
        select_time()
    else:
        print(selected_movie_id,selected_hall_id,selected_show_id)
        selected_movie_id=0
        selected_hall_id=0
        selected_show_id=0
        print(selected_movie_id,selected_hall_id,selected_show_id)
        show_movie_list()

#############################################################################################
def select_hall():
    connectDB()
    query='select ch_id,ch_name,ch_loc from cinema_hall'
    mycursor.execute(query)
    hall_list=mycursor.fetchall()
    if len(hall_list)==0:
        messagebox.showinfo('Error','No cinema hall Found')
    else:
        def button_clicked(event):
            button = event.widget
            button_data = button_data_dict[button]
            global selected_hall_id
            selected_hall_id=int(button_data['text'])
            global selected_hall_name
            selected_hall_name=button_data['name']
            print("Button clicked - Name:", selected_hall_name,"hall id =" ,selected_hall_id)

        destroy_dialog_frame()
        global dialog_frame
        dialog_frame = Frame(home_window,width=650,height=350,bg=sc_color)
        dialog_frame.place(x=50,y=200)
        s_movie='selected movie : '+selected_movie_name
        label2=Label(dialog_frame,text=s_movie, font=("Arial", 12),bg=sc_color,width=72,height=2)
        label2.place(x=0,y=0)
        Label(dialog_frame,text="Select Cinema hall", font=("Arial", 12),bg=sc_color,width=72,height=2).place(x=0,y=36)

        button_data_dict = {}
        chid=0
        i,j=0,0
        for i, hall in enumerate(hall_list):
            for j, value in enumerate(hall):
                a=80+40*i
                b=20+200*(j-1)

                bttn_name='button'+str(i)
                if j==0:
                    chid=value
                    continue
                elif j==1:
                    bttn_name = Button(dialog_frame, text=value,name=bttn_name, font=("Arial", 12),bd=0,bg=sc_color)
                    button_data_dict[bttn_name] = {'name': value, 'text': chid}
                    bttn_name.place(x=b,y=a)
                    bttn_name.bind("<Button-1>", button_clicked)
                else:
                    label = Label(dialog_frame, text=value, font=("Arial", 12),bd=0,bg=sc_color)
                    label.place(x=b,y=a)
                

        close_button = Button(dialog_frame, text="Confirm", command=destroy_hall_frame)
        close_button.place(x=300,y=300)
    con.close()

def destroy_hall_frame():
    if selected_hall_id==0:
        messagebox.showerror('error','No hall selected')
    else:
        messagebox.showinfo('Selected',selected_hall_name)
        dialog_frame.destroy()
        select_time()

####################################################################################
def select_time():
    connectDB()
    query='select show_id,show_date,start_time,end_time from show_time where movie_id=%s and ch_id=%s'
    mycursor.execute(query,(selected_movie_id,selected_hall_id))
    show_list=mycursor.fetchall()
    if len(show_list)== 0:
        destroy_dialog_frame()
        global dialog_frame
        dialog_frame = Frame(home_window,width=650,height=350,bg=sc_color)
        dialog_frame.place(x=50,y=200)
        label3=Label(dialog_frame,text="this movie is not running on this cinema hall\nchoose other cinema hall", font=("Arial", 16),justify="center",bg=sc_color)
        label3.place(x=100,y=100)
        close_button = Button(dialog_frame, text="Go back", command=select_hall_again)
        close_button.place(x=300,y=300)
    else:
        def button_clicked(event):
            button = event.widget
            button_data = button_data_dict[button]
            global selected_show_id
            selected_show_id=int(button_data['text'])
            print("Button clicked - Showtime selected and ","show id =" ,selected_show_id)

        destroy_dialog_frame()
        dialog_frame = Frame(home_window,width=650,height=350,bg=sc_color)
        dialog_frame.place(x=50,y=200)

        s_movie='selected movie : '+selected_movie_name
        s_hall='selected cinema hall : '+selected_hall_name
        label3=Label(dialog_frame,text=s_movie, font=("Arial", 12),bg=sc_color,width=72,height=2)
        label3.place(x=0,y=0)
        Label(dialog_frame,text=s_hall, font=("Arial", 12),bg=sc_color,width=72,height=2).place(x=0,y=36)
        Label(dialog_frame,text="Select show time", font=("Arial", 12),bg=sc_color,width=72,height=2).place(x=0,y=72)

        button_data_dict = {}
        showid=0
        i,j=0,0
        for i, row in enumerate(show_list):
            for j, value in enumerate(row):
                a=120+40*i
                b=20+150*(j-1)

                bttn_name='button'+str(i)
                if j==0:
                    showid=value
                    continue
                else:
                    label = Label(dialog_frame, text=value, font=("Arial", 12),bd=0,bg=sc_color)
                    label.place(x=b,y=a)
                bttn_name = Button(dialog_frame, text='select',name=bttn_name, font=("Arial", 12),bd=0,bg=sc_color)
                button_data_dict[bttn_name] = {'name': bttn_name, 'text': showid}
                bttn_name.place(x=b+150,y=a-7)
                bttn_name.bind("<Button-1>", button_clicked)

        close_button = Button(dialog_frame, text="Confirm", command=destroy_fr3)
        close_button.place(x=300,y=300)
    con.close()

def select_hall_again():
    dialog_frame.destroy()
    select_hall()

def destroy_fr3():
    if selected_show_id==0:
        messagebox.showerror('error','No time slot selected')
    else:
        messagebox.showinfo('Selected','select seats now')
        dialog_frame.destroy()
        seat()

#######################################################################################
def seat():
    global seat_list
    seat_list=[]
    connectDB()
    query='select * from seat2 where show_id=%s'
    global selected_hall_id
    mycursor.execute(query,(selected_show_id))
    rows=mycursor.fetchall()
    if len(rows)==0:
        messagebox.showinfo('Error','no seat info available')
    else:
        def button_clicked(event):
            button = event.widget
            button.config(bg="purple")
            button_data = button_data_dict[button]
            global selected_seat_id
            selected_seat_id=int(button_data['seatid'])
            global selected_seat_no
            selected_seat_no=button_data['seatno']
            global selected_seat_status
            selected_seat_status=button_data['status']
            global seat_list
            seat_list.append(selected_seat_id)
            print("Button clicked - seat no:", selected_seat_no,"seat id =" ,selected_seat_id)

        global dialog_frame
        dialog_frame=Frame(home_window,width=650,height=580, bg=sc_color)
        dialog_frame.place(x=50,y=140)
        Label(dialog_frame,text="screen this way", font=("Arial", 12),bg='lightblue',width=75,height=2).place(x=0,y=0)
        Label(dialog_frame,text="seat available", font=("Arial", 12),bg='green',width=25).place(x=0,y=42)
        Label(dialog_frame,text="booked already", font=("Arial", 12),bg='red',width=25).place(x=200,y=42)
        Label(dialog_frame,text="you selected", font=("Arial", 12),bg='purple',width=25).place(x=420,y=42)

        button_data_dict = {}
        sid,sno,st=0,0,0
        i,j=0,0
        a,b=0,0
        r,c=0,0
        for i, row in enumerate(rows):
            if i%10==0:
                r=0
                c+=1
            b=40+60*r
            r+=1
            a=70+40*c
            for j, value in enumerate(row):
                if j==0:
                    sid=value
                elif j==1:
                    st=value
                elif j==2:
                    sno=value
        
            bttn_name='button'+str(i)
            if st==0:
                bttn_name = Button(dialog_frame, text=sno,name=bttn_name, font=("Arial", 12),bd=0,bg='green',width=5)
                button_data_dict[bttn_name] = {'seatno': sno, 'seatid': sid, 'status':st}
                bttn_name.place(x=b,y=a)
                bttn_name.bind("<Button-1>", button_clicked)
            elif st==1:
                bttn_name = Button(dialog_frame, text=sno,name=bttn_name, font=("Arial", 12),bd=0,bg='red',width=5)
                bttn_name.place(x=b,y=a)

        close_button = Button(dialog_frame, text="  Confirm   ", command=destroy_seat_frame)
        close_button.place(x=300,y=540)
    con.close()

def destroy_seat_frame():
    dialog_frame.destroy()
    connectDB()
    new_st=1
    global seat_list
    print('seat booked by id',seat_list)
    query='UPDATE seat2 SET status=%s WHERE seat_id = %s;'
    for s_id in seat_list:
        mycursor.execute(query,(new_st,s_id))
    disconnectDB()
    if len(seat_list)!=0:
        messagebox.showinfo('successful','Go for payment')
        Payment()

####################################################################################
def Payment():
######################################
    #creating ticked id and ticket table updation
    connectDB()
    query='select * from tickets'
    mycursor.execute(query)
    ticket_list=mycursor.fetchall()
    t_list=[]
    for i in ticket_list:
        if i[0] != None:
            t_list.append(i[0])
    print(t_list)
    print(max(t_list))
    new_ticket_id=max(t_list)+1
    global selected_ticket_id
    selected_ticket_id=new_ticket_id
    print('hello test: t_id new : ',new_ticket_id)

    query='select movie_type from movies where movie_id=%s'
    mycursor.execute(query,(selected_movie_id))
    movie_type=mycursor.fetchone()

    query='select show_date,start_time,end_time,ticket_price from show_time where show_id=%s'
    mycursor.execute(query,(selected_show_id))
    show_datas=mycursor.fetchone()

    query='select ch_name,ch_loc from cinema_hall where ch_id=%s'
    mycursor.execute(query,(selected_hall_id))
    hall_datas=mycursor.fetchone()
    
    query='SELECT DAYNAME(%s) AS day_of_week'
    mycursor.execute(query,(show_datas[0]))
    show_dayy=mycursor.fetchone()
    
    if show_dayy!=None and movie_type!=None and show_datas!=None and hall_datas!=None:
        print('ticket creation done')
        print(new_ticket_id,new_ticket_id,selected_movie_name,movie_type[0],show_datas[0],show_dayy[0],show_datas[1],show_datas[2],show_datas[3],selected_hall_name,hall_datas[1] ,len(seat_list),len(seat_list)*show_datas[3], selected_user_name)
        query='insert into tickets(ticket_id,ticket_no,movie_name,movie_type,show_date,show_day,start_time,end_time,ticket_price,ch_name,ch_loc,no_of_seats,price,username) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        mycursor.execute(query,(new_ticket_id,new_ticket_id,selected_movie_name,movie_type[0],show_datas[0],show_dayy[0],show_datas[1],show_datas[2],show_datas[3],selected_hall_name,hall_datas[1] ,len(seat_list),len(seat_list)*show_datas[3], selected_user_name))
    
    disconnectDB()
######################################
    #booking table updation
    connectDB()
    query='select * from booking'
    mycursor.execute(query)
    booking_list=mycursor.fetchall()
    b_list=[]
    for i in booking_list:
        if i[0] != None:
            b_list.append(i[0])
    print(b_list)
    print(max(b_list))
    new_book_id=max(b_list)+1
    book_status=0
    for seat_id in seat_list:
        print('booking done')
        query='insert into booking(book_id,movie_id,ch_id,show_id,book_status,seat_id,ticket_id) values (%s,%s,%s,%s,%s,%s,%s)'
        mycursor.execute(query,(new_book_id,selected_movie_id,selected_hall_id,selected_show_id,book_status,seat_id,selected_ticket_id))
        new_book_id+=1
    disconnectDB()
######################################
    #rest payment frame
    print('all booking done')

    global dialog_frame
    dialog_frame=Frame(home_window,width=650,height=350, bg=sc_color)
    dialog_frame.place(x=50,y=200)
    Label(dialog_frame,text="Pay Now", font=("Arial", 12),bg='lightblue',width=75,height=2).place(x=0,y=0)

    Label(dialog_frame,text="choose one option", font=("Arial", 12),bg='white',height=2).place(x=240,y=100)
    Button(dialog_frame,text="online banking", font=("Arial", 12),bg='green',width=25,command=gen_ticket).place(x=200,y=150)
    Button(dialog_frame,text="credit/debit card", font=("Arial", 12),bg='red',width=25,command=gen_ticket).place(x=200,y=200)
    Button(dialog_frame,text="UPI", font=("Arial", 12),bg='purple',width=25,command=gen_ticket).place(x=200,y=250)
    Button(dialog_frame,text="pay later", font=("Arial", 12),bg='white',width=25,command=destroy_dialog_frame).place(x=200,y=300)

#####################################################################################################
#CANCEL TICKETS  
def cancel_ticket():
    t_id=selected_ticket_id
    print('tid inside cancel ticket :',t_id)
    destroy_dialog_frame()

    connectDB()
    query='DELETE FROM booking WHERE ticket_id=%s'
    mycursor.execute(query,(t_id))
    query='DELETE FROM tickets WHERE ticket_id=%s'
    mycursor.execute(query,(t_id))
    disconnectDB()
    messagebox.showinfo(':(','ticket cancelled')
    print('cancellation successful')


######################################################################
#printing the ticket
def ticket(t_id):
    connectDB()
    query='select * from tickets where ticket_id=%s'
    print('selected_ticket_id inside ticket: ',t_id, 'type :', type(t_id))
    mycursor.execute(query,(t_id))
    ticket_data=mycursor.fetchone()
    print(ticket_data)
    disconnectDB()
    if ticket_data!=None:
        destroy_dialog_frame()
        global dialog_frame
        dialog_frame=Frame(home_window,width=650,height=350, bg=sc_color)
        dialog_frame.place(x=50,y=200)

        heading_label=Label(dialog_frame,text='Ticket',fg='red',bg=sc_color,font=('Microsoft YaHei UI Light',14,'bold'))
        heading_label.grid(row=0,column=1)
        t_no='No. '+str(ticket_data[1])
        ticket_no=Label(dialog_frame,text=t_no,fg='black',bg=sc_color,font=('Microsoft YaHei UI Light',8,'bold'))
        ticket_no.grid(row=0,column=2)

        movie_label=Label(dialog_frame,text='Movie Name : ',fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',font_size,'bold'))
        movie_label.grid(row=1,column=0,sticky='w',padx=25,pady=(10,10))
        movie_name=Label(dialog_frame,text=ticket_data[2],fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',font_size,'bold'))
        movie_name.grid(row=1,column=1,sticky='w',padx=25,pady=(10,10))
        movie_type=Label(dialog_frame,text=ticket_data[3],fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',font_size,'bold'))
        movie_type.grid(row=1,column=2,sticky='w',padx=25,pady=(10,10))

        time_label=Label(dialog_frame,text='Date & Time : ',fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',font_size,'bold'))
        time_label.grid(row=2,column=0,sticky='w',padx=25,pady=(10,10))
        date_name=Label(dialog_frame,text=ticket_data[4],fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',font_size,'bold'))
        date_name.grid(row=2,column=1,sticky='w',padx=25,pady=(10,10))
        day_name=Label(dialog_frame,text=ticket_data[5],fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',font_size,'bold'))
        day_name.grid(row=2,column=2,sticky='w',padx=25,pady=(10,10))
        timee=str(ticket_data[6])+' - '+str(ticket_data[7])
        time_name=Label(dialog_frame,text=timee,fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',font_size,'bold'))
        time_name.grid(row=3,column=1,sticky='w',padx=25,pady=(10,10))

        theater_label=Label(dialog_frame,text='theater Name : ',fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',font_size,'bold'))
        theater_label.grid(row=4,column=0,sticky='w',padx=25,pady=(10,10))
        theater_name=Label(dialog_frame,text=ticket_data[9],fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',font_size,'bold'))
        theater_name.grid(row=4,column=1,sticky='w',padx=25,pady=(10,10))
        #theater_location=Label(dialog_frame,text='Location',fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',18,'bold'))
        #theater_location.grid(row=5,column=0,sticky='w',padx=25,pady=(10,10))
        theater_loc=Label(dialog_frame,text=ticket_data[10],fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',font_size,'bold'))
        theater_loc.grid(row=4,column=2,sticky='w',padx=25,pady=(10,10))

        seat_label=Label(dialog_frame,text='Seat details : ',fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',font_size,'bold'))
        seat_label.grid(row=5,column=0,sticky='w',padx=25,pady=(10,10))
        no_s='no of seats : '+str(ticket_data[11])
        seat_no=Label(dialog_frame,text=no_s,fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',font_size,'bold'))
        seat_no.grid(row=5,column=1,sticky='w',padx=25,pady=(10,10))
        seat_de='seat no : xx,yy,zz'
        seats=Label(dialog_frame,text=seat_de,fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',font_size,'bold'))
        seats.grid(row=6,column=1,sticky='w',padx=25,pady=(10,10))

        price=Label(dialog_frame,text='Price : ',fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',font_size,'bold'))
        price.grid(row=7,column=0,sticky='w',padx=25,pady=(10,10))
        amount=Label(dialog_frame,text=ticket_data[12],fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',font_size,'bold'))
        amount.grid(row=7,column=1,sticky='w',padx=25,pady=(10,10))

        user=Label(dialog_frame,text='Ticket booked by :',fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',font_size,'bold'))
        user.grid(row=8,column=0,sticky='w',padx=25,pady=(10,10))
        username=Label(dialog_frame,text=ticket_data[13],fg=pr_color,bg=sc_color,font=('Microsoft YaHei UI Light',font_size,'bold'))
        username.grid(row=8,column=1,sticky='w',padx=25,pady=(10,10))

        backbutton=Button(dialog_frame,text='cancel ticket',bd=0,bg=sc_color,activebackground=sc_color,cursor='hand2',font=("Arial", 12),command=cancel_ticket)
        backbutton.grid(row=9,column=1,sticky='w',padx=25,pady=(10,10))

        #pdf
        tktpdf=f'___________________Ticket__________________{t_no}\n\n'
        tktpdf+=f'Movie Name : {ticket_data[2]}\n'
        tktpdf+=f'Movie Type : {ticket_data[2]}\n'
        tktpdf+=f'Movie Name : {ticket_data[3]}\n'
        tktpdf+=f'Date & Time : {ticket_data[4]}\n'
        print(tktpdf)
        pdf_path = 'report.pdf'
        pdf = canvas.Canvas(pdf_path, pagesize=letter)  

        x, y = 50, 750
        pdf.drawString(x, y, str(tktpdf))

        pdf.save()

#####################################################################################################
def gen_ticket():                     #module after payment
    destroy_dialog_frame()
    ####################################
    connectDB()
    for seat in seat_list:
        query='UPDATE booking SET book_status=1 WHERE seat_id = %s;'
        mycursor.execute(query,(seat))
        query='UPDATE booking SET u_id=%s WHERE seat_id = %s;'
        mycursor.execute(query,(selected_user_id,seat))
    disconnectDB()
    print('updation of status and user done')
    ####################################
    messagebox.showinfo('Successful','Payment done successfully')

    ## the ticket
    ticket(selected_ticket_id)

#######################################################
#payment button on header
def pay2():
    global dialog_frame
    dialog_frame=Frame(home_window,width=650,height=350, bg=sc_color)
    dialog_frame.place(x=50,y=200)
    Label(dialog_frame,text="Pay Now", font=("Arial", 12),bg='lightblue',width=75,height=2).place(x=0,y=0)

    Label(dialog_frame,text="choose one option", font=("Arial", 12),bg='white',height=2).place(x=240,y=100)
    Button(dialog_frame,text="online banking", font=("Arial", 12),bg='green',width=25,command=gen_ticket).place(x=200,y=150)
    Button(dialog_frame,text="credit/debit card", font=("Arial", 12),bg='red',width=25,command=gen_ticket).place(x=200,y=200)
    Button(dialog_frame,text="UPI", font=("Arial", 12),bg='purple',width=25,command=gen_ticket).place(x=200,y=250)
    Button(dialog_frame,text="pay later", font=("Arial", 12),bg='white',width=25,command=destroy_dialog_frame).place(x=200,y=300)

def go_to_payment():
    destroy_dialog_frame()
    global dialog_frame
    dialog_frame=Frame(home_window,width=650,height=350, bg=sc_color)
    dialog_frame.place(x=50,y=200)
    Label(dialog_frame,text="Pending Payments", font=("Arial", 12),bg='lightblue',width=75,height=2).place(x=0,y=0)

    connectDB()
    query='select distinct ticket_id from booking where book_status=0 and ticket_id in (select ticket_id from tickets where username in (select username from user_data where u_id=%s))'
    mycursor.execute(query,(selected_user_id))
    unpaid_books=mycursor.fetchall()

    t_list=[]
    for i,seat in enumerate(unpaid_books):
            for j,val in enumerate(seat):
                if val != None:
                    t_list.append(val)
    print(t_list)

    
    query='select seat_id from booking where book_status=0 and ticket_id in (select ticket_id from tickets where username in (select username from user_data where u_id=%s))'
    mycursor.execute(query,(selected_user_id))
    unpaid_seats=mycursor.fetchall()
    
    print(unpaid_seats)

    s_list=[]
    for i,seat in enumerate(unpaid_seats):
            for j,val in enumerate(seat):
                if val != None:
                    s_list.append(val)
    print(s_list)

    ticket_data_dict = {}
    if unpaid_books==None:
        messagebox.showinfo('yahoo!!','no pending payments')
    else: 
        def button_clicked(event):
            button = event.widget
            button_data = ticket_data_dict[button]
            global selected_ticket_id
            selected_ticket_id=int(button_data['t_id'])
            print("Button clicked - tid =" ,selected_ticket_id)
            
            connectDB()
            query='select seat_id from booking where ticket_id=%s'
            mycursor.execute(query,(selected_ticket_id))
            un_seats=mycursor.fetchall()
            print(un_seats)
            disconnectDB()

            s_id_list=[]
            for i,seat in enumerate(un_seats):
                    for j,val in enumerate(seat):
                        if val != None:
                            s_id_list.append(val)
            print(s_id_list)

            global seat_list
            seat_list=s_id_list
            pay2()

        a,b,i=0,0,0
        for val in t_list:
            connectDB()
            query='select ticket_no,movie_name,ch_name from tickets where ticket_id=%s'
            mycursor.execute(query,(val))
            data=mycursor.fetchone()
            disconnectDB()
            a=50
            b=100+30*i
            bttn_name='button'+str(i)
            data0=str(i+1)
            data1='ticket no: '+str(data[0])
            data2=str(data[1])+', '+str(data[2])
            data3=data[0]
            Label(dialog_frame, text=data0, font=("Arial", 12),bd=0,bg=sc_color).place(x=a,y=b)
            Label(dialog_frame, text=data1, font=("Arial", 12),bd=0,bg=sc_color).place(x=a+40,y=b)
            Label(dialog_frame, text=data2, font=("Arial", 12),bd=0,bg=sc_color).place(x=a+140,y=b)
            bttn_name=Button(dialog_frame, text='select', font=("Arial", 12),bd=0,bg=sc_color)
            ticket_data_dict[bttn_name] = {'name': bttn_name, 't_id': data3}
            bttn_name.place(x=a+460,y=b)
            bttn_name.bind("<Button-1>", button_clicked)
            i+=1
            '''
            query='UPDATE booking SET book_status=1 WHERE seat_id = %s;'
            mycursor.execute(query,(seat))
            query='UPDATE booking SET u_id=%s WHERE seat_id = %s;'
            mycursor.execute(query,(selected_user_id,seat))
            '''
    disconnectDB()

#################################################################
#ticket button on header
def show_booked_tickets():
    destroy_dialog_frame()
    global dialog_frame
    dialog_frame=Frame(home_window,width=650,height=350, bg=sc_color)
    dialog_frame.place(x=50,y=200)
    Label(dialog_frame,text="tickets booked", font=("Arial", 12),bg='lightblue',width=75,height=2).place(x=0,y=0)
    connectDB()
    query='select distinct ticket_id from booking where book_status=1 and u_id=%s'
    mycursor.execute(query,(selected_user_id))
    booked_ticket=mycursor.fetchall()

    ticket_data_dict = {}
    if len(booked_ticket)==0:
        messagebox.showinfo('oops!!','no show booked')
    else: 
        def button_clicked(event):
            button = event.widget
            button_data = ticket_data_dict[button]
            global selected_ticket_id
            selected_ticket_id=int(button_data['t_id'])
            print("Button clicked - button no:",button_data['name'],"tid =" ,selected_ticket_id)
            ticket(selected_ticket_id)
            
        a,b=0,0
        for i,seat in enumerate(booked_ticket):
            for j,val in enumerate(seat):
                if val != None:
                    query='select ticket_no,movie_name,ch_name from tickets where ticket_id=%s'
                    mycursor.execute(query,(val))
                    data=mycursor.fetchone()
                    a=50
                    b=100+30*i
                    bttn_name='button'+str(i)
                    data0=str(i+1)
                    data1='ticket no: '+str(data[0])
                    data2=str(data[1])+', '+str(data[2])
                    data3=data[0]
                    Label(dialog_frame, text=data0, font=("Arial", 12),bd=0,bg=sc_color).place(x=a,y=b)
                    Label(dialog_frame, text=data1, font=("Arial", 12),bd=0,bg=sc_color).place(x=a+40,y=b)
                    Label(dialog_frame, text=data2, font=("Arial", 12),bd=0,bg=sc_color).place(x=a+140,y=b)
                    bttn_name=Button(dialog_frame, text='select', font=("Arial", 12),bd=0,bg=sc_color)
                    ticket_data_dict[bttn_name] = {'name': bttn_name, 't_id': data3}
                    bttn_name.place(x=a+460,y=b)
                    bttn_name.bind("<Button-1>", button_clicked)
        
    disconnectDB()

####################################################################################
#home window
home_window=Tk()
home_window.title('home')
home_window.geometry('1380x776+0+0')
home_window.configure(bg='#fff')
home_window.resizable(False,False)

#background image
bg_img = ImageTk.PhotoImage(Image.open(path1))
bg_label=Label(home_window, image =bg_img, bg=sc_color)
bg_label.grid()


#top-over frame
dialog_frame= None

#heading
heading_frame=Frame(home_window,width=1380,height=40, bg=tr_color)
heading_frame.place(x=0,y=0)

heading =Label(heading_frame,text='Multiplex Ticket Booking System',fg=sc_color,bg=tr_color,font=('Microsoft YaHei UI Light',18,'bold'),bd=0)
heading.place(x=500,y=0)

#search
search_frame=Frame(home_window,width=1380,height=40, bg=tr_color)
search_frame.place(x=0,y=92)

s0_label=Button(search_frame,text=' ',font=('Microsoft YaHei UI Light',10,'bold'),bd=0,bg=tr_color,fg=tr_color,width=30)
s0_label.grid(row=1,column=0,sticky='w',padx=25,pady=(10,10))

search_label=Entry(search_frame,text='Search Movie',font=('Microsoft YaHei UI Light',10,'bold'),bg=sc_color,fg=pr_color,width=50)
search_label.grid(row=1,column=1,sticky='w',padx=25,pady=(10,10))
search_label.insert(0,'Search Movie')
search_label.bind('<FocusIn>',userEnter)

search_button=Button(search_frame,text=search_label.get(),font=('Microsoft YaHei UI Light',10,'bold'),bd=0,bg=sc_color,fg=pr_color,activebackground=pr_color,activeforeground=sc_color,cursor='hand2',command=search_movie)
search_button.grid(row=1,column=2,sticky='w',padx=25,pady=(10,10))

s1_label=Button(search_frame,text=' ',font=('Microsoft YaHei UI Light',10,'bold'),bd=0,bg=tr_color,fg=tr_color,width=80)
s1_label.grid(row=1,column=3,sticky='w',padx=25,pady=(10,10))

#body
body_frame=Frame(home_window,width=1380,height=40, bg=sc_color)
body_frame.place(x=0,y=40)

#search movie
#book ticket
#show ticket
#order food
#payment
a0_label=Button(body_frame,text=' ',font=('Microsoft YaHei UI Light',10,'bold'),bd=0,bg=sc_color,fg=pr_color,width=30)
a0_label.grid(row=0,column=0,sticky='w',padx=25,pady=(10,10))
a1_label=Button(body_frame,text='Movie List',font=('Microsoft YaHei UI Light',10,'bold'),bg=sc_color,fg=pr_color,command=show_movie_list)
a1_label.grid(row=0,column=1,sticky='w',padx=25,pady=(10,10))

a2_label=Button(body_frame,text='Book Tickets',font=('Microsoft YaHei UI Light',10,'bold'),bg=sc_color,fg=pr_color,command=movie_book)
a2_label.grid(row=0,column=2,sticky='w',padx=25,pady=(10,10))

a3_label=Button(body_frame,text='Cinema halls',font=('Microsoft YaHei UI Light',10,'bold'),bg=sc_color,fg=pr_color,command=show_hall_list)
a3_label.grid(row=0,column=3,sticky='w',padx=25,pady=(10,10))

a4_label=Button(body_frame,text='Order Food',font=('Microsoft YaHei UI Light',10,'bold'),bg=sc_color,fg=pr_color)
a4_label.grid(row=0,column=4,sticky='w',padx=25,pady=(10,10))

a5_label=Button(body_frame,text='Payment',font=('Microsoft YaHei UI Light',10,'bold'),bg=sc_color,fg=pr_color,command=go_to_payment)
a5_label.grid(row=0,column=5,sticky='w',padx=25,pady=(10,10))

a6_label=Button(body_frame,text='tickets',font=('Microsoft YaHei UI Light',10,'bold'),bg=sc_color,fg=pr_color,command=show_booked_tickets)
a6_label.grid(row=0,column=6,sticky='w',padx=25,pady=(10,10))

a7_label=Button(body_frame,text='  ',font=('Microsoft YaHei UI Light',10,'bold'),bd=0,bg=sc_color,fg=pr_color, width=30)
a7_label.grid(row=0,column=7,sticky='w',padx=25,pady=(10,10))

u_label=Button(heading_frame,text='User',font=('Microsoft YaHei UI Light',10,'bold'),bd=0,bg='black',fg=sc_color, width=20, height=2,command=show_user_data)
u_label.place(x=0,y=0)


#footer
footer_frame=Frame(home_window,width=1380,height=60, bg=sc_color)
footer_frame.place(x=0,y=723)

f0_label=Button(footer_frame,text=' ',font=('Microsoft YaHei UI Light',10,'bold'),bd=0,bg=sc_color,fg=pr_color,width=50)
f0_label.grid(row=0,column=0,sticky='w',padx=25,pady=(10,10))

f5_label=Button(footer_frame,text='Home',font=('Microsoft YaHei UI Light',10,'bold'),bg=sc_color,fg=pr_color, command=destroy_dialog_frame)
f5_label.grid(row=0,column=1,sticky='w',padx=25,pady=(10,10))

f1_label=Button(footer_frame,text='About Us',font=('Microsoft YaHei UI Light',10,'bold'),bg=sc_color,fg=pr_color, command=show_aboutus)
f1_label.grid(row=0,column=2,sticky='w',padx=25,pady=(10,10))

f2_label=Button(footer_frame,text='  Contacts  ',font=('Microsoft YaHei UI Light',10,'bold'),bg=sc_color,fg=pr_color,command=show_contact)
f2_label.grid(row=0,column=3,sticky='w',padx=25,pady=(10,10))

f3_label=Button(footer_frame,text='  FAQs  ',font=('Microsoft YaHei UI Light',10,'bold'),bg=sc_color,fg=pr_color, command=show_faq)
f3_label.grid(row=0,column=4,sticky='w',padx=25,pady=(10,10))

f4_label=Button(footer_frame,text='  ',font=('Microsoft YaHei UI Light',10,'bold'),bg=sc_color,fg=pr_color,bd=0,width=80)
f4_label.grid(row=0,column=5,sticky='w',padx=25,pady=(10,10))




home_window.mainloop()








# movie->select_hall()->select_time()->seat()->payment()->gen_ticket()->ticket()
#show_booked_tickets() -> cancel_ticket(t_id) -> ticket_clicked(tid)
