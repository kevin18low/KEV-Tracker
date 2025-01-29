from django.shortcuts import render
import mysql.connector
from .KEV_script import script
from dotenv import load_dotenv
import os

load_dotenv()

# Render selected table with optional filters
def run(request, table, condition):
    db = mysql.connector.connect(
    host=os.environ.get('HOST'),
    user=os.environ.get('USER'),
    passwd=os.environ.get('PW'),
    database=os.environ.get('DB')
    )   

    cursor = db.cursor()

    query = f"SELECT * FROM {table} {condition}"

    cursor.execute(query)
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

# Render KEV_Catalog table
def kev(request):
    return run(request, "KEV_Catalog", "")

# Render Event_log table
def log(request):
    return run(request, "Event_log", "")

# Render appropriate table filtered by user keyword search
def search(request):
    # Check if either search bar has an input
    log_search = request.GET.get('log-search', '')
    kev_search = request.GET.get('kev-search', '')
    
    if log_search:
        table = "Event_log"
        search_term = log_search
    elif kev_search:
        table = "KEV_Catalog"
        search_term = kev_search
    else:
        return run(request, "KEV_Catalog", "")

    db = mysql.connector.connect(
        host=os.environ.get('HOST'),
        user=os.environ.get('USER'),
        passwd=os.environ.get('PW'),
        database=os.environ.get('DB')
    )   

    cursor = db.cursor()

    # Get column names
    cursor.execute(f"SHOW COLUMNS FROM {table}")
    columns = [col[0] for col in cursor.fetchall()]

    # Build WHERE clause according to user input
    where_clause = " OR ".join([f"LOWER({col}) LIKE LOWER('%{search_term}%')" for col in columns])

    query = f"SELECT * FROM {table} WHERE {where_clause}"
    
    # Render filtered table
    return run(request, table, f"WHERE {where_clause}")

# Manually download latest KEV Catalog and refresh page
def refresh(request):
    script.create_table_from_csv()
    return run(request, "KEV_Catalog", "")