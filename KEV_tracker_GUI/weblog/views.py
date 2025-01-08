from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="kevin",
    passwd="klow05_SQL_**",
    database="CISA-KEV"
    )   
print("Connected")

cursor = db.cursor()

cursor.execute("SELECT * FROM Event_log")
rows = cursor.fetchall()

# Extract column names from cursor.description
columns = [col[0] for col in cursor.description]

# List to store each log
logs = []

# Convert each row into a dictionary and append to the list
for row in rows:
    row_dict = dict(zip(columns, row))  # Convert row to dictionary
    logs.append(row_dict)     # Append to the list

def home(request):
    context = {
        'logs': logs
    }
    return render(request, 'weblog/home.html', context)
