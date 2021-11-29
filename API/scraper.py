import csv
import requests
import pytz
from datetime import datetime, timezone
import sqlite3
import sys


CO2_URL = 'https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_trend_gl.csv'
DATABASE = './output-table.db'

def test():
    print ("scrape test")

def write_to_db(ts, s, t):

    try:
        conn = sqlite3.connect(DATABASE)
        print ("[Scraper] Connected to db")

        # Check if the output table exits
        # check count of table entries
        cursor = conn.cursor()
        cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='output' ''')

        assert (cursor.fetchone()[0] == 1), "Output Table must exist"

        # Table exists, UPDATE entries            
        records_to_update = [(ts, s, "smoothed"), (ts, t, "trend")]
        sql_update_q = """UPDATE output set timestamp=?, co2_ppm=? WHERE parameter=? """
        cursor.executemany(sql_update_q, records_to_update)
        conn.commit()

        print ("Total number of rows updated :", conn.total_changes)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to update multiple records of sqlite table, quitting", error)
        sys.exit("Failed to create/write into output table")

    finally:
        if conn:
            conn.close()
            print("The DB connection is closed")



def scrape():

    with requests.Session() as s:
        print ("Downloading NOAA data from ", CO2_URL)
        download = s.get(CO2_URL)
        decoded_content = download.content.decode('utf-8')
        data = csv.reader(decoded_content.splitlines(), delimiter = ',')
        lastEntry = list(data)[-1]

        # Format of csv file is as follows
        # Year , month, date, smoothed, trend

        s = float(lastEntry[3])
        t = float(lastEntry[4])

        tz_ca = pytz.timezone('US/Pacific')

        dt = datetime(int(lastEntry[0]), int(lastEntry[1]), int(lastEntry[2]), 0, 0, 0, tzinfo=tz_ca)
        print ("time : ", int(dt.timestamp()))
        print ("s =", s)
        print ("t = ", t)

        write_to_db(int(dt.timestamp()), s, t)

if __name__ == "__main__":
    scrape()
    