from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import re
import mysql.connector
import pymysql

mydb = mysql.connector.connect(host='localhost',user='root',password='password',database="softwareProject")

class AdminPg:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1500x800+0+0")
        self.root.title("Admin Page")
        img = Image.open("D:\\projectX\\assets\\background_images\\BG2.jpeg")
        img = img.resize((1400,800),Image.Resampling.LANCZOS)
        self.image_bg = ImageTk.PhotoImage(img)
        self.label_bg_image=Label(root,image=self.image_bg)
        self.label_bg_image.place(x=0,y=0,relwidth=1,relheight=1)


        self.heading = Label(text="MULTIPLEX MANAGEMENT SYSTEM",font=("times new roman",20,"bold"),bg='yellow',fg="red")
        self.heading.place(x=400,y=30)

        Movie_button=Button(self.root,text="Add Movie",bg="white",font=("time new roman",15,"bold"),activeforeground="white",activebackground="white",command=self.addmovie)
        Movie_button.place(x=100,y=60)

        Cinema_button=Button(self.root,text="Add Multiplex",bg="white",font=("time new roman",15,"bold"),activeforeground="white",activebackground="white",command=self.addMultiplex)
        Cinema_button.place(x=100,y=110)

        ShowTime_button=Button(self.root,text="Add Show Time and Date",bg="white",font=("time new roman",15,"bold"),activeforeground="white",activebackground="white",command=self.addmovieTimedate)
        ShowTime_button.place(x=100,y=160)

        Snacks_button=Button(self.root,text="Add Snacks",bg="white",font=("time new roman",15,"bold"),activeforeground="white",activebackground="white",command=self.addSnacksItem)
        Snacks_button.place(x=100,y=210)
        
        Show_Movie=Button(self.root,text="Show All Movie",bg="white",font=("time new roman",15,"bold"),activeforeground="white",activebackground="white",command=self.showMovie)
        Show_Movie.place(x=100,y=260)
        
        Show_Multiplex=Button(self.root,text="Show All Multiplex",bg="white",font=("time new roman",15,"bold"),activeforeground="white",activebackground="white",command=self.showMultiplex)
        Show_Multiplex.place(x=100,y=310)

        Show_datetime=Button(self.root,text="Movies Date and Time",bg="white",font=("time new roman",15,"bold"),activeforeground="white",activebackground="white",command=self.showDateTime)
        Show_datetime.place(x=100,y=360)

        Show_Snacks=Button(self.root,text="Show Snacks Item",bg="white",font=("time new roman",15,"bold"),activeforeground="white",activebackground="white",command=self.showSnacksItem)
        Show_Snacks.place(x=100,y=410)

        delete_Movie=Button(self.root,text="Delete Movie",bg="white",font=("time new roman",15,"bold"),activeforeground="white",activebackground="white",command=self.deleteMovie)
        delete_Movie.place(x=100,y=460)

        delete_cinema=Button(self.root,text="Delete Cinema Hall",bg="white",font=("time new roman",15,"bold"),activeforeground="white",activebackground="white",command=self.deleteCinema)
        delete_cinema.place(x=100,y=510)

        delete_DateTime=Button(self.root,text="Delete show",bg="white",font=("time new roman",15,"bold"),activeforeground="white",activebackground="white",command=self.deleteDateTime)
        delete_DateTime.place(x=100,y=560)

        delete_Snacks=Button(self.root,text="Delete Snacks Item",bg="white",font=("time new roman",15,"bold"),activeforeground="white",activebackground="white",command=self.deletesnack)
        delete_Snacks.place(x=100,y=610)

        show_tickets=Button(self.root,text="show booked tickets",bg="white",font=("time new roman",15,"bold"),activeforeground="white",activebackground="white",command=self.show_tickets)
        show_tickets.place(x=100,y=660)

        cancel_shows=Button(self.root,text="cancel show",bg="white",font=("time new roman",15,"bold"),activeforeground="white",activebackground="white",command=self.cancel_shows)
        cancel_shows.place(x=100,y=710)

        reset_seats=Button(self.root,text="create seats/reset seats",bg="white",font=("time new roman",15,"bold"),activeforeground="white",activebackground="white",command=self.reset_seat)
        reset_seats.place(x=100,y=760)

    def reset_seat(self):
        try:
            con=pymysql.connect(host='localhost',user='root',password='Surajit@123')
            mycursor=con.cursor()
        except:
            messagebox.showerror('Error','Database connectivity error. Try again.')
        query='use softwareProject'
        mycursor.execute(query)
        query='select show_id,ch_id from show_time'
        mycursor.execute(query)
        rows=mycursor.fetchall()

        show_dict={}
        show_id,ch_id=0,0
        for i,row in enumerate(rows):
            for j,value in enumerate(row):
                if j==0:
                    show_id=value
                else:
                    ch_id=value
            show_dict[i]={'show_id':show_id,'ch_id':ch_id}

        seat_cap={}
        query='select seat_capacity from cinema_hall where ch_id = %s'
        for ch_id in show_dict:
            mycursor.execute(query,(ch_id))
            row=mycursor.fetchone()
            if row != None:
                seat_cap[ch_id]=row[0]

        print(seat_cap)

        for i in range(len(show_dict)):
            show_dict[i]['s_cap']=seat_cap[show_dict[i]['ch_id']]


        total_seat=0
        for i in show_dict:
            for j in range(1,show_dict[i]['s_cap']+1):
                total_seat+=1
        print(total_seat)

        query='select seat_id from seat2'
        mycursor.execute(query)
        row=mycursor.fetchall()
        print(len(row))

        if total_seat != len(row):
            st_id=total_seat+1
            new_st=0
            query='insert into seat2 values (%s,%s,%s,%s,%s)'
            for i in show_dict:
                s_no=1
                if i == len(show_dict)-1:
                    for j in range(1,show_dict[i]['s_cap']+1):
                        mycursor.execute(query,(st_id,new_st,s_no,show_dict[i]['ch_id'],show_dict[i]['show_id']))
                        st_id+=1
                        s_no+=1
        else:
            query='drop table seat2'
            mycursor.execute(query)
            st_id=1
            new_st=0
            query='insert into seat2 values (%s,%s,%s,%s,%s)'
            for i in show_dict:
                s_no=1
                for j in range(1,show_dict[i]['s_cap']+1):
                    mycursor.execute(query,(st_id,new_st,s_no,show_dict[i]['ch_id'],show_dict[i]['show_id']))
                    st_id+=1
                    s_no+=1

        con.commit()
        mycursor.close()
        con.close()
        messagebox.showinfo('success','seat creation/reset successful')

    def showMovie(self):
        self.my_w = Tk()
        self.my_w.geometry("1500x800+0+0") 
        self.my_conn = mydb.cursor()
        self.my_conn.execute("SELECT * FROM movies")
        i=0 
        for m in self.my_conn: 
            for j in range(len(m)):
                e = Entry(self.my_w, width=25, fg='blue') 
                e.grid(row=i, column=j) 
                e.insert(END, m[j])
            i=i+1
        self.my_w.mainloop()

    def show_tickets(self):
        self.my_w = Tk()
        self.my_w.geometry("1500x800+0+0") 
        self.my_conn = mydb.cursor()
        self.my_conn.execute("SELECT * FROM tickets")
        i=0 
        for m in self.my_conn: 
            for j in range(len(m)):
                e = Entry(self.my_w, width=25, fg='blue') 
                e.grid(row=i, column=j) 
                if m[j]== None:
                    e.insert(END, 'null')
                else:
                    e.insert(END, m[j])
            i=i+1
        self.my_w.mainloop()

    def showMultiplex(self):
        self.my_w = Tk()
        self.my_w.geometry("1500x800+0+0") 
        self.my_conn = mydb.cursor()
        self.my_conn.execute("SELECT * FROM cinema_hall")
        i=0 
        for m in self.my_conn: 
            for j in range(len(m)):
                e = Entry(self.my_w, width=25, fg='blue') 
                e.grid(row=i, column=j) 
                e.insert(END, m[j])
            i=i+1
        self.my_w.mainloop()

    def showDateTime(self):
        self.my_w = Tk()
        self.my_w.geometry("1500x800+0+0") 
        self.my_conn = mydb.cursor()
        self.my_conn.execute("SELECT * FROM show_time")
        i=0 
        for m in self.my_conn: 
            for j in range(len(m)):
                e = Entry(self.my_w, width=25, fg='blue') 
                e.grid(row=i, column=j) 
                e.insert(END, m[j])
            i=i+1
        self.my_w.mainloop()
    
    def showSnacksItem(self):
        self.my_w = Tk()
        self.my_w.geometry("1500x800+0+0") 
        self.my_conn = mydb.cursor()
        self.my_conn.execute("SELECT * FROM food")
        i=0 
        for m in self.my_conn: 
            for j in range(len(m)):
                e = Entry(self.my_w, width=25, fg='blue') 
                e.grid(row=i, column=j) 
                e.insert(END, m[j])
            i=i+1
        self.my_w.mainloop()

    def deleteMovie(self):
        self.frame1 = Frame(self.root,bg="grey")
        self.frame1.place(x=280,y=120,width="970",height="450")

        self.id = Label(self.frame1,text="Movie Id",font=("times new roman",25,"bold"),fg="white",bg="grey")
        self.id.place(x=300,y=100)        
        self.textname1 = Entry(self.frame1,font=("times new roman",25,"bold"))
        self.textname1.place(x=300,y=160,width=250)

        self.delete_button=Button(self.frame1,text="Delete Data",bg="white",font=("time new roman",25,"bold"),activeforeground="white",activebackground="white",command=self.delete_store1)       
        self.delete_button.place(x=300,y=250)

        self.close_button=Button(self.frame1,text="close",bg="white",font=("time new roman",25,"bold"),activeforeground="white",activebackground="white",command=self.frame1.destroy)       
        self.close_button.place(x=800,y=250)

    def delete_store1(self):
        a = self.textname1.get()
        self.cur = mydb.cursor()
        self.s = "delete from movies where movie_id = %s"
        self.cur.execute(self.s,(a,))
        mydb.commit()
        self.frame1.destroy()
        messagebox.showinfo('success','movie info deleted')

    def cancel_shows(self):
        self.frame1 = Frame(self.root,bg="grey")
        self.frame1.place(x=280,y=120,width="970",height="450")

        self.id = Label(self.frame1,text="show Id",font=("times new roman",25,"bold"),fg="white",bg="grey")
        self.id.place(x=300,y=100)        
        self.textname1 = Entry(self.frame1,font=("times new roman",25,"bold"))
        self.textname1.place(x=300,y=160,width=250)

        self.delete_button=Button(self.frame1,text="cancel all tickets",bg="white",font=("time new roman",25,"bold"),activeforeground="white",activebackground="white",command=self.delete_store11)       
        self.delete_button.place(x=300,y=250)

        self.close_button=Button(self.frame1,text="close",bg="white",font=("time new roman",25,"bold"),activeforeground="white",activebackground="white",command=self.frame1.destroy)       
        self.close_button.place(x=800,y=250)

    def delete_store11(self):
        a = self.textname1.get()
        self.cur = mydb.cursor()
        self.s = "delete from booking where show_id = %s"
        self.cur.execute(self.s,(a,))
        self.s = "delete from tickets where ticket_id in (select ticket_id from booking where show_id=%s);"
        self.cur.execute(self.s,(a,))
        self.s = "delete from seat2 where show_id =%s;"
        self.cur.execute(self.s,(a,))
        self.s = "delete from show_time where show_id =%s;"
        self.cur.execute(self.s,(a,))
        mydb.commit()
        self.frame1.destroy()
        messagebox.showinfo('success','show info, related tickets deleted')

    def deleteCinema(self):
        self.frame1 = Frame(self.root,bg="grey")
        self.frame1.place(x=280,y=120,width="970",height="450")

        self.id = Label(self.frame1,text="Cinema Id",font=("times new roman",25,"bold"),fg="white",bg="grey")
        self.id.place(x=300,y=100)        
        self.textname1 = Entry(self.frame1,font=("times new roman",25,"bold"))
        self.textname1.place(x=300,y=160,width=250)

        self.delete_button=Button(self.frame1,text="Delete Data",bg="white",font=("time new roman",25,"bold"),activeforeground="white",activebackground="white",command=self.delete_store2)       
        self.delete_button.place(x=300,y=250)

        self.close_button=Button(self.frame1,text="close",bg="white",font=("time new roman",25,"bold"),activeforeground="white",activebackground="white",command=self.frame1.destroy)       
        self.close_button.place(x=800,y=250)

    def delete_store2(self):
        a = self.textname1.get()
        self.cur = mydb.cursor()
        self.s = "delete from cinema_hall where ch_id = %s"
        self.cur.execute(self.s,(a,))
        mydb.commit()
        self.frame1.destroy()
        messagebox.showinfo('success','cinema hall info deleted')

    def deleteDateTime(self):
        self.frame1 = Frame(self.root,bg="grey")
        self.frame1.place(x=280,y=120,width="970",height="450")

        self.id = Label(self.frame1,text="Show Id",font=("times new roman",25,"bold"),fg="white",bg="grey")
        self.id.place(x=300,y=100)        
        self.textname1 = Entry(self.frame1,font=("times new roman",25,"bold"))
        self.textname1.place(x=300,y=160,width=250)

        self.delete_button=Button(self.frame1,text="Delete Data",bg="white",font=("time new roman",25,"bold"),activeforeground="white",activebackground="white",command=self.delete_store3)       
        self.delete_button.place(x=300,y=250)

        self.close_button=Button(self.frame1,text="close",bg="white",font=("time new roman",25,"bold"),activeforeground="white",activebackground="white",command=self.frame1.destroy)       
        self.close_button.place(x=800,y=250)

    def delete_store3(self):
        a = self.textname1.get()
        self.cur = mydb.cursor()
        self.s = "delete from show_time where show_id = %s"
        self.cur.execute(self.s,(a,))
        mydb.commit()
        self.frame1.destroy()
        messagebox.showinfo('success','show info deleted')

    def deletesnack(self):
        self.frame1 = Frame(self.root,bg="grey")
        self.frame1.place(x=280,y=120,width="970",height="450")

        self.id = Label(self.frame1,text="Snack Id",font=("times new roman",25,"bold"),fg="white",bg="grey")
        self.id.place(x=300,y=100)        
        self.textname1 = Entry(self.frame1,font=("times new roman",25,"bold"))
        self.textname1.place(x=300,y=160,width=250)

        self.delete_button=Button(self.frame1,text="Delete Data",bg="white",font=("time new roman",25,"bold"),activeforeground="white",activebackground="white",command=self.delete_store4)       
        self.delete_button.place(x=300,y=250)

        self.close_button=Button(self.frame1,text="close",bg="white",font=("time new roman",25,"bold"),activeforeground="white",activebackground="white",command=self.frame1.destroy)       
        self.close_button.place(x=800,y=250)

    def delete_store4(self):
        a = self.textname1.get()
        self.cur = mydb.cursor()
        self.s = "delete from food where food_id = %s"
        self.cur.execute(self.s,(a,))
        mydb.commit()
        self.frame1.destroy()
        messagebox.showinfo('success','food item deleted')

    def addmovie(self):
        self.frame1 = Frame(self.root,bg="grey")
        self.frame1.place(x=280,y=120,width="970",height="450")

        self.id = Label(self.frame1,text="Movie Id",font=("times new roman",25,"bold"),fg="white",bg="grey")
        self.id.place(x=50,y=60)        
        self.textname1 = Entry(self.frame1,font=("times new roman",25,"bold"))
        self.textname1.place(x=230,y=60,width=250)

        self.movieName = Label(self.frame1,text="Movie Name",font=("times new roman",25,"bold"),fg="white",bg="grey")
        self.movieName.place(x=490,y=60)        
        self.textname2 = Entry(self.frame1,font=("times new roman",25,"bold"))
        self.textname2.place(x=690,y=60,width=250)

        self.description = Label(self.frame1,text="Description",font=("times new roman",25,"bold"),fg="white",bg="grey")
        self.description.place(x=50,y=130)        
        self.textname3 = Entry(self.frame1,font=("times new roman",25,"bold"))
        self.textname3.place(x=230,y=130,width=250)

        self.Duration = Label(self.frame1,text="Duration",font=("times new roman",25,"bold"),fg="white",bg="grey")
        self.Duration.place(x=490,y=130)        
        self.textname4 = Entry(self.frame1,font=("times new roman",25,"bold"))
        self.textname4.place(x=690,y=130,width=250)

        self.Language = Label(self.frame1,text="Language",font=("times new roman",25,"bold"),fg="white",bg="grey")
        self.Language.place(x=50,y=210)        
        self.textname5 = Entry(self.frame1,font=("times new roman",25,"bold"))
        self.textname5.place(x=230,y=210,width=250)

        self.Release = Label(self.frame1,text="Release",font=("times new roman",25,"bold"),fg="white",bg="grey")
        self.Release.place(x=490,y=210)        
        self.textname6 = Entry(self.frame1,font=("times new roman",25,"bold"))
        self.textname6.place(x=690,y=210,width=250)

        self.Country = Label(self.frame1,text="Country",font=("times new roman",25,"bold"),fg="white",bg="grey")
        self.Country.place(x=50,y=290)        
        self.textname7 = Entry(self.frame1,font=("times new roman",25,"bold"))
        self.textname7.place(x=230,y=290,width=250)

        self.Genre = Label(self.frame1,text="Genre",font=("times new roman",25,"bold"),fg="white",bg="grey")
        self.Genre.place(x=490,y=290)        
        self.textname8 = Entry(self.frame1,font=("times new roman",25,"bold"))
        self.textname8.place(x=690,y=290,width=250)

        self.mtype = Label(self.frame1,text="movie type",font=("times new roman",25,"bold"),fg="white",bg="grey")
        self.mtype.place(x=50,y=370)        
        self.textname9 = Entry(self.frame1,font=("times new roman",25,"bold"))
        self.textname9.place(x=230,y=370,width=250)

        self.Add_button=Button(self.frame1,text="Add Data",bg="white",font=("time new roman",25,"bold"),activeforeground="white",activebackground="white",command=self.store1)       
        self.Add_button.place(x=550,y=350)

        self.close_button=Button(self.frame1,text="close",bg="white",font=("time new roman",25,"bold"),activeforeground="white",activebackground="white",command=self.frame1.destroy)       
        self.close_button.place(x=800,y=350)

    def store1(self):
        a,b,c,d,e,f,g,h,i=(self.textname1.get(),self.textname2.get(),self.textname3.get(),self.textname4.get(),self.textname5.get(),self.textname6.get(),self.textname7.get(),self.textname8.get(),self.textname9.get())

        self.cur = mydb.cursor()
        self.s="INSERT INTO movies VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.b1 = (a,b,c,d,e,f,g,h,i)
        self.cur.execute(self.s,self.b1)
        mydb.commit()
        self.frame1.destroy()
        messagebox.showinfo('success','movie info added')

    def addMultiplex(self):
        self.frame1 = Frame(self.root,bg="grey")
        self.frame1.place(x=280,y=120,width="970",height="450")

        self.id = Label(self.frame1,text="Cinema Id",font=("times new roman",25,"bold"),fg="white",bg="grey")
        self.id.place(x=150,y=60)        
        self.textname1 = Entry(self.frame1,font=("times new roman",25,"bold"))
        self.textname1.place(x=380,y=60,width=250)

        self.movieName = Label(self.frame1,text="Cinema Name",font=("times new roman",25,"bold"),fg="white",bg="grey")
        self.movieName.place(x=150,y=120)        
        self.textname2 = Entry(self.frame1,font=("times new roman",25,"bold"))
        self.textname2.place(x=380,y=120,width=250)

        self.description = Label(self.frame1,text="Description",font=("times new roman",25,"bold"),fg="white",bg="grey")
        self.description.place(x=150,y=180)        
        self.textname3 = Entry(self.frame1,font=("times new roman",25,"bold"))
        self.textname3.place(x=380,y=180,width=250)

        self.Duration = Label(self.frame1,text="Location",font=("times new roman",25,"bold"),fg="white",bg="grey")
        self.Duration.place(x=150,y=240)        
        self.textname4 = Entry(self.frame1,font=("times new roman",25,"bold"))
        self.textname4.place(x=380,y=240,width=250)

        self.seat_cap = Label(self.frame1,text="seat capacity",font=("times new roman",25,"bold"),fg="white",bg="grey")
        self.seat_cap.place(x=150,y=300)        
        self.textname5 = Entry(self.frame1,font=("times new roman",25,"bold"))
        self.textname5.place(x=380,y=300,width=250)
       
        self.Add_button=Button(self.frame1,text="Add Data",bg="white",font=("time new roman",25,"bold"),activeforeground="white",activebackground="white",command=self.store2)       
        self.Add_button.place(x=400,y=370)

        self.close_button=Button(self.frame1,text="close",bg="white",font=("time new roman",25,"bold"),activeforeground="white",activebackground="white",command=self.frame1.destroy)       
        self.close_button.place(x=800,y=370)

    def store2(self):
        a,b,c,d,e=(self.textname1.get(),self.textname2.get(),self.textname3.get(),self.textname4.get(),self.textname5.get())

        self.cur = mydb.cursor()
        self.s="INSERT INTO cinema_hall VALUES(%s,%s,%s,%s,%s)"
        self.b1 = (a,b,c,d,e)
        self.cur.execute(self.s,self.b1)
        mydb.commit()
        self.frame1.destroy()
        messagebox.showinfo('success','cinema hall info added')

    def addmovieTimedate(self):
        self.frame1 = Frame(self.root,bg="grey")
        self.frame1.place(x=280,y=120,width="970",height="450")

        self.id = Label(self.frame1,text="Show Id",font=("times new roman",25,"bold"),fg="white",bg="grey")
        self.id.place(x=50,y=60)        
        self.textname1 = Entry(self.frame1,font=("times new roman",25,"bold"))
        self.textname1.place(x=230,y=60,width=250)

        self.movieName = Label(self.frame1,text="Show Date",font=("times new roman",25,"bold"),fg="white",bg="grey")
        self.movieName.place(x=490,y=60)        
        self.textname2 = Entry(self.frame1,font=("times new roman",25,"bold"))
        self.textname2.place(x=690,y=60,width=250)

        self.description = Label(self.frame1,text="Start Time",font=("times new roman",25,"bold"),fg="white",bg="grey")
        self.description.place(x=50,y=130)        
        self.textname3 = Entry(self.frame1,font=("times new roman",25,"bold"))
        self.textname3.place(x=230,y=130,width=250)

        self.Duration = Label(self.frame1,text="End Time",font=("times new roman",25,"bold"),fg="white",bg="grey")
        self.Duration.place(x=490,y=130)        
        self.textname4 = Entry(self.frame1,font=("times new roman",25,"bold"))
        self.textname4.place(x=690,y=130,width=250)

        self.Language = Label(self.frame1,text="Cinema Id",font=("times new roman",25,"bold"),fg="white",bg="grey")
        self.Language.place(x=50,y=210)        
        self.textname5 = Entry(self.frame1,font=("times new roman",25,"bold"))
        self.textname5.place(x=230,y=210,width=250)

        self.Release = Label(self.frame1,text="Movie Id",font=("times new roman",25,"bold"),fg="white",bg="grey")
        self.Release.place(x=490,y=210)        
        self.textname6 = Entry(self.frame1,font=("times new roman",25,"bold"))
        self.textname6.place(x=690,y=210,width=250)

        self.Relea = Label(self.frame1,text="ticket price",font=("times new roman",25,"bold"),fg="white",bg="grey")
        self.Relea.place(x=50,y=290)        
        self.textname7 = Entry(self.frame1,font=("times new roman",25,"bold"))
        self.textname7.place(x=230,y=290,width=250)

        self.Add_button=Button(self.frame1,text="Add Data",bg="white",font=("time new roman",25,"bold"),activeforeground="white",activebackground="white",command=self.store3)       
        self.Add_button.place(x=400,y=380)

        self.close_button=Button(self.frame1,text="close",bg="white",font=("time new roman",25,"bold"),activeforeground="white",activebackground="white",command=self.frame1.destroy)       
        self.close_button.place(x=800,y=380)
    

    def store3(self):
        a,b,c,d,e,f,g=(self.textname1.get(),self.textname2.get(),self.textname3.get(),self.textname4.get(),self.textname5.get(),self.textname6.get(),self.textname7.get())

        self.cur = mydb.cursor()
        self.s="INSERT INTO show_time VALUES(%s,%s,%s,%s,%s,%s,%s)"
        self.b1 = (a,b,c,d,e,f,g)
        self.cur.execute(self.s,self.b1)
        mydb.commit()
        self.frame1.destroy()
        messagebox.showinfo('success','show info added')

    def addSnacksItem(self):
        self.frame1 = Frame(self.root,bg="grey")
        self.frame1.place(x=280,y=120,width="970",height="450")

        self.id = Label(self.frame1,text="Snacks Id",font=("times new roman",25,"bold"),fg="white",bg="grey")
        self.id.place(x=150,y=60)        
        self.textname1 = Entry(self.frame1,font=("times new roman",25,"bold"))
        self.textname1.place(x=380,y=60,width=250)

        self.movieName = Label(self.frame1,text="Snacks Name",font=("times new roman",25,"bold"),fg="white",bg="grey")
        self.movieName.place(x=150,y=120)        
        self.textname2 = Entry(self.frame1,font=("times new roman",25,"bold"))
        self.textname2.place(x=380,y=120,width=250)

        self.description = Label(self.frame1,text="Description",font=("times new roman",25,"bold"),fg="white",bg="grey")
        self.description.place(x=150,y=180)        
        self.textname3 = Entry(self.frame1,font=("times new roman",25,"bold"))
        self.textname3.place(x=380,y=180,width=250)

        self.Duration = Label(self.frame1,text="Price",font=("times new roman",25,"bold"),fg="white",bg="grey")
        self.Duration.place(x=150,y=240)        
        self.textname4 = Entry(self.frame1,font=("times new roman",25,"bold"))
        self.textname4.place(x=380,y=240,width=250)
       
        self.Add_button=Button(self.frame1,text="Add Data",bg="white",font=("time new roman",25,"bold"),activeforeground="white",activebackground="white",command=self.store4)       
        self.Add_button.place(x=280,y=330)

        self.close_button=Button(self.frame1,text="close",bg="white",font=("time new roman",25,"bold"),activeforeground="white",activebackground="white",command=self.frame1.destroy)       
        self.close_button.place(x=800,y=330)
    
    def store4(self):
        a,b,c,d=(self.textname1.get(),self.textname2.get(),self.textname3.get(),self.textname4.get())

        self.cur = mydb.cursor()
        self.s="INSERT INTO food VALUES(%s,%s,%s,%s)"
        self.b1 = (a,b,c,d)
        self.cur.execute(self.s,self.b1)
        mydb.commit()
        self.frame1.destroy()
        messagebox.showinfo('success','food item added')



if __name__== "__main__":
    root=Tk()
    app=AdminPg(root)
    root.mainloop()
