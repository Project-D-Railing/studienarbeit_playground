import pymysql

# Open database connection
db = pymysql.connect("localhost","homestead","secret","homestead" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
sql = "SELECT haltestellen2.name FROM zuege2,haltestellen2 where zuege2.evanr=haltestellen2.eva_nr AND zugid like '%6957575484712982863-1711301729%'"
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Fetch all the rows in a list of lists.
   results = cursor.fetchall()
   for row in results:
      somevariablename = row[0]
      # Now somevariablenameprint fetched result
      print (somevariablename)
except:
   print ("Error: unable to fetch data")

# disconnect from server
db.close()
