
# This script is to scrape all the data off the CSV files. It should be run after
# reset.py, as there will be a conflict between existing tables if it is not.
# The script creates a database with the name "stocks.db" with all the info for
# accessing later.
# Script also generates a "tickers.json" file containing all the tickers used.
# This is for looping through the different tables in the db later.

# AUTHOR: Daniel Hernandez H.
# LICENSE: MIT License (https://opensource.org/licenses/MIT)

import os
import sqlite3
import json

# path to access stock quote files
basepath = "../raw_data/daily/"

# connect with database
conn = sqlite3.connect("stocks.db")
cur = conn.cursor()

# for reference later on
ticker_list = []

# loop through all the .csv files in the directory with raw data
for csv in os.listdir(basepath):
    if csv.endswith(".csv"):
        # extracts the stock ticker from filename
        ticker = (csv[csv.index("_") + 1:csv.index(".")]).upper()

        ticker_list.append(ticker)

        print "Processing", ticker, "..."

        fh = open(basepath + csv)

        # SQL command to create new tables. Quotes around ticker
        # to escape key words (e.g ALL)
        sql_command = "CREATE TABLE " + "'" + ticker + "'" + " (date INTEGER UNIQUE, open REAL, close REAL, high REAL, low REAL, volume REAL)"

        cur.execute(sql_command)

        for line in fh:

            line = line.strip().split(",")

            # grabbing data we need from CSV file
            date = line[0]
            # skipping index 1 because it is not needed
            open_val = line[2]
            high = line[3]
            low = line[4]
            close_val = line[5]
            volume = line[6]

            # again escaping the ticker
            sql_insert = "INSERT INTO " + "'" + ticker + "'" + " VALUES (?, ?, ?, ?, ?, ?) "

            cur.execute(sql_insert, (date, open_val, close_val, high, low, volume) )

        conn.commit()

        print ticker, "done"

ticker_json = json.dumps(ticker_list, indent=4)

json_file = open("tickers.json", "w")

json_file.write(ticker_json)

json_file.close()
