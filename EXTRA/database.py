#creating seat 
import pymysql
from tkinter import messagebox
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

#print(show_dict)
print(seat_cap)

for i in range(len(show_dict)):
    show_dict[i]['s_cap']=seat_cap[show_dict[i]['ch_id']]

#print(show_dict) 

total_seat=0
for i in show_dict:
    for j in range(1,show_dict[i]['s_cap']+1):
        total_seat+=1
print(total_seat)

query='select seat_id from seat2'
mycursor.execute(query)
row=mycursor.fetchall()
print(len(row))

'''
#seat creation from beggining

st_id=1
new_st=0
query='insert into seat2 values (%s,%s,%s,%s,%s)'
for i in show_dict:
    s_no=1
    for j in range(1,show_dict[i]['s_cap']+1):
        mycursor.execute(query,(st_id,new_st,s_no,show_dict[i]['ch_id'],show_dict[i]['show_id']))
        st_id+=1
        s_no+=1
'''

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
#con.commit()
mycursor.close()
con.close()