import pymysql
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Connect to the MySQL database
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='Surajit@123',
    database='softwareproject'
)

# Fetch data from the SQL table
cursor = connection.cursor()
cursor.execute('SELECT * FROM tickets where ticket_id=3')
data = cursor.fetchall()

# Create a PDF document
pdf_path = 'report.pdf'
pdf = canvas.Canvas(pdf_path, pagesize=letter)


###########################################################################################
row_val=['ticket id : ','ticket no : ', 'movie name : ', 'movie type : ', 'show date : ', 'day : ', 'start time : ', 'end time : ', 'ticket price : ', 'cinema hall : ', 'hall location : ', 'no of price : ', 'total bill: ', 'booked by : ']
pdf.drawString(400, 800, 'Ticket')

###########################################################################################

# Set the starting position for drawing
x, y = 250, 750

pdf.drawString(x+50,y, 'Ticket')
y-=50
# Iterate over the fetched data and write it to the PDF
'''
for row in data:
    for column in row:
        pdf.drawString(x, y, str(column))
        x += 100  # Increase the x-coordinate for the next column
    y -= 20  # Decrease the y-coordinate for the next row
    x = 50  # Reset the x-coordinate for the next row
'''
i=0
for row in data:
    for column in row:
        pdf.drawString(x-200, y, str(row_val[i]))
        pdf.drawString(x, y, str(column))
        y -= 20
        i +=1
    x = 50  # Reset the x-coordinate for the next row

# Save and close the PDF document
pdf.save()

# Close the database connection
connection.close()

print("PDF generated successfully!")
