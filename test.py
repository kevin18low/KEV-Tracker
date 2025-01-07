import schedule
import time
from urllib.request import urlretrieve

url = "https://www.cisa.gov/sites/default/files/csv/known_exploited_vulnerabilities.csv"
csv_file_path = '/home/kevin/Downloads/known_exploited_vulnerabilities.csv'

def download_csv():
    path, headers = urlretrieve(url, csv_file_path)
    date_accessed = headers.get("Date")
    print("KEV file downloaded: " + date_accessed)

schedule.every(3).seconds.do(download_csv)

while True:
    schedule.run_pending()
    time.sleep(1)

