from django.shortcuts import render
import mysql.connector

def home(request):
    db = mysql.connector.connect(
    host="localhost",
    user="kevin",
    passwd="klow05_SQL_**",
    database="CISA-KEV"
)

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

    context = {
        'logs': logs
    }
    return render(request, 'weblog/home.html', context)
