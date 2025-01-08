from django.shortcuts import render
import mysql.connector

def run(request, table):
    db = mysql.connector.connect(
    host="localhost",
    user="kevin",
    passwd="klow05_SQL_**",
    database="CISA-KEV"
    )   

    cursor = db.cursor()

    cursor.execute("SELECT * FROM " + table)
    rows = cursor.fetchall()

    # Extract column names from cursor.description
    columns = [col[0] for col in cursor.description]

    # List to store each log
    logs = []

    # Convert each row into a dictionary and append to the list
    for row in rows:
        row_dict = dict(zip(columns, row))  # Convert row to dictionary
        if table == "KEV_Catalog":
            logs.append(row_dict)     # Append to the list
        elif table == "Event_log":
            logs.insert(0, row_dict)     # Insert to front of the list
        
    context = {
        'cols': columns,
        'logs': logs
    }

    if table == "KEV_Catalog":
        return render(request, 'weblog/kev.html', context)
    elif table == "Event_log":
        return render(request, 'weblog/log.html', context)

def kev(request):
    return run(request, "KEV_Catalog")

def log(request):
    return run(request, "Event_log")
