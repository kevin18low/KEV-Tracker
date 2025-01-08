import mysql.connector
import csv
import schedule
import time
from urllib.request import urlretrieve

if __name__ == "__main__":
    db = mysql.connector.connect(
        host="localhost",
        user="kevin",
        passwd="klow05_SQL_**",
        database="CISA-KEV"
        )

    if db.is_connected():
        print("Connected to database")   

    cursor = db.cursor()

    def create_log_table():
        table_query = "CREATE TABLE IF NOT EXISTS Event_log ("
        columns = "Status VARCHAR(255) NOT NULL, Time VARCHAR(255) NOT NULL, NewRecords int NOT NULL );"
        table_query += columns
        cursor.execute(table_query)
        print("Eventlog table created successfully")

    # CISA download link for KEV catalog
    url = "https://www.cisa.gov/sites/default/files/csv/known_exploited_vulnerabilities.csv"

    # Filepath to downloaded csv
    csv_file_path = '/home/kevin/Downloads/known_exploited_vulnerabilities.csv'

    # Download csv from CISA website
    def download_csv():
        path, headers = urlretrieve(url, csv_file_path)
        date_accessed = headers.get("Date")
        print("KEV file downloaded: " + date_accessed)
        return date_accessed

    # Determine datatype for each table column
    def data_type(data):
        try:
            int(data)
            return "INT"
        except ValueError:
            try:
                float(data)
                return "FLOAT"
            except ValueError:
                return "TEXT"

    # Create table with all columns included in csv file 
    def create_table_from_csv():
        status = "Failed"
        time = download_csv()
        # Open CSV file and read the header
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            headers = reader.fieldnames
            
            # Generate CREATE TABLE query
            create_table_query = f"CREATE TABLE IF NOT EXISTS KEV_Catalog ("
            
            for header in headers:    
                create_table_query += f"{header} {data_type('')},"  # Add each column
            create_table_query = create_table_query.rstrip(',') + ');'  # Remove trailing comma and close query

            # Execute the query to create the table
            cursor.execute(create_table_query)
            print("KEV table updated successfully.")
            
            cursor.execute("SELECT COUNT(*) FROM KEV_Catalog")
            old_data_count = cursor.fetchone()[0]
            cursor.execute("TRUNCATE TABLE KEV_Catalog") # Delete old data before inserting new
            # Insert CSV data into the table
            insert_query = f"INSERT INTO KEV_Catalog ({', '.join(headers)}) VALUES ({', '.join(['%s'] * len(headers))})"
            
            for row in reader:
                values = tuple(row[field] for field in headers)
                cursor.execute(insert_query, values)

            status = "Success"       

            # Count total entries and calculate number of new entries
            cursor.execute("SELECT COUNT(*) FROM KEV_Catalog")
            new_data_count = cursor.fetchone()[0]

            new_records = new_data_count - old_data_count

            # Update event log for each attempted catalog update
            cursor.execute(f"INSERT INTO Event_log (Status, Time, NewRecords) VALUES ('{status}', '{time}', '{new_records}')")

            # Commit the transaction and notify if new KEV's were added
            db.commit()
            print(f"KEV catalog updated. Inserted {new_records} new vulnerabilities.\n")   

    create_log_table()  # Set up empty event log table

    interval = input("How often (hours) do you want to update the KEV_Catalog? ")
    try:
        interval = float(interval)
    except:
        print("Your input was invalid. The interval has been set to the default 4 hours.")
        interval = 4

    create_table_from_csv()
    schedule.every(interval).hours.do(create_table_from_csv)

    # Download and update database every n hours
    def run(n):
        schedule.run_pending()
        n *= 3600
        time.sleep(n) # Sleep until just before next interval

    while True:
        run(interval)