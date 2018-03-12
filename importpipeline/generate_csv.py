import sys
import mysqldb 
import csv

mydb = mysqldb.connect(host='localhost',
    user='',
    passwd='',
    db='')
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
print "Query executed."
print "Wrote %s rows to csv." % cursor.rowcount 