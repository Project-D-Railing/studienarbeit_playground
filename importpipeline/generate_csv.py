import sys
import pymysql
import csv
import json

# open config file with database access and some other stuff
with open('config.json', 'r') as f:
    config = json.load(f)
    
# TODO create functions for query and parsing and preprocessing and write to csv    
    
# connect to database
mydb = pymysql.connect(config['host'],config['user'],config['password'],config['database'])
cursor = mydb.cursor()

## query
query = ("SELECT * FROM zuege2 WHERE datum='2018-03-12' ")
cursor.execute(query)

### write to csv file

# Generate switch by mode and int of entries per file
# e.g.  test, 1000
# or    train, 20000
# for predict use other db with entries which should be predicted coming from a web interface or other tool

csv_writer = csv.writer(open("./train/CSV_Output.csv", "wt")) # create csv
csv_writer.writerow([i[0] for i in cursor.description]) # write headers
csv_writer.writerows(cursor) # write records
del csv_writer # close csv file

cursor.close()
mydb.close()
print("Query executed.")
print("Wrote %s rows to csv." % cursor.rowcount)