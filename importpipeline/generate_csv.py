import sys
import pymysql
import csv
import datetime
import json
import re

# used by arzeitist,arzeitsoll,dpzeitist,dpzeitsoll
def timetotimeint(input):
    input = str(input)
    # first check all times if they are none
    if input == 'None':
     input = "00:00:-01"
       
    # now all times are 'valid' ehhrrmmm
    # convert tome to integer none values are now negative numbers like -1
    hhmmss = input
    (h, m, s) = hhmmss.split(':')
    result = int(h) * 3600 + int(m) * 60 + int(s)
    return result

    
#used instead of hash buckets to get a better idea of the meaing of the values  
#warning this function is slow
def coloumntovocalfileold(name,input):
    # ii#
    filename = "./vocabfiles/" + str(name) + ".txt"
    with open(filename, "r+") as file:
        for line in file:
            if input in line:
                break
        else: # not found, we are at the eof
            file.write(input) # append missing data
    

def openvocalfile(name):
    # ii#
    lines = []
    filename = "./vocabfiles/" + str(name) + ".txt"
    with open(filename, "w+") as file:
        for line in file:
            line = line.rstrip('\n')
            lines.append(line)
    return lines    
    
def writevocalfile(name,vocab):
    # ii#
    lines = vocab
    filename = "./vocabfiles/" + str(name) + ".txt"
    with open(filename, "w+") as file:
        for item in lines:
            file.write("%s\n" % item)
         
# open config file with database access and some other stuff
with open('config.json', 'r') as f:
    config = json.load(f)
    
# TODO create functions for query and parsing and preprocessing and write to csv    
    
# connect to database
mydb = pymysql.connect(config['host'],config['user'],config['password'],config['database'])
cursor = mydb.cursor()

## query
query = ("SELECT * FROM zuege2 WHERE datum='2018-03-12' AND evanr=8000191")


### write to csv file

# Generate switch by mode and int of entries per file
# e.g.  test, 1000
# or    train, 20000
# for predict use other db with entries which should be predicted coming from a web interface or other tool
csv_writer = csv.writer(open("./train/CSV_Output.csv", "wt", newline="\n", encoding="utf-8")) # create csv
try:
   # Execute the SQL command
   cursor.execute(query)
   # Fetch all the rows in a list of lists.
   results = cursor.fetchall()
   
   csv_writer.writerow([i[0] for i in cursor.description]) # write headers
   
   zugklasse_vocab = openvocalfile('zugklasse')
   zugowner_vocab = openvocalfile('zugowner')
   linie_vocab = openvocalfile('linie')
   gleisist_vocab = openvocalfile('gleisist')
   gleissoll_vocab = openvocalfile('gleissoll')

   #print(zugklasse_vocab)
   for row in results:
      id = row[0]
      zugid = row[1]
      zugverkehrstyp = row[2]
      zugtyp = row[3]
      zugowner = row[4]
      zugklasse = row[5]
      zugnummer = row[6]
      zugnummerfull = row[7]
      linie = row[8]
      evanr = row[9]
      arzeitsoll = row[10]
      arzeitist = row[11]
      dpzeitsoll = row[12]
      dpzeitist = row[13]
      gleissoll = row[14]
      gleisist = row[15]
      datum = row[16]
      streckengeplanthash = row[17]
      streckenchangedhash = row[18]
      zugstatus = row[19]
      # begin preprocessing

      # preprocess zugid
      #this regex matchges zugid into 3 groups
      match = re.match(r"(\-*[0-9]*)\-([0-9]*)\-([0-9]*)$", zugid)
      someint = match.group(1)
      sometime = match.group(2)
      stopnumber = match.group(3)
      #print(stopnumber)
      
      # preprocess times in function
      arzeitsoll = timetotimeint(arzeitsoll)
      arzeitist = timetotimeint(arzeitist)
      dpzeitsoll = timetotimeint(dpzeitsoll)
      dpzeitist = timetotimeint(dpzeitist)
      
      # preprocess zugowner
      if zugowner not in zugowner_vocab:
        #print('Fehlt')
        zugowner_vocab.append(zugowner)
      
      # preprocess zugklasse
      if zugklasse not in zugklasse_vocab:
        #print('Fehlt')
        zugklasse_vocab.append(zugklasse)

      # preprocess linie
      if linie not in linie_vocab:
        #print('Fehlt')
        linie_vocab.append(linie)

      # preprocess gleisist,gleissoll
      if gleisist not in gleisist_vocab:
        #print('Fehlt')
        gleisist_vocab.append(gleisist)

      if gleissoll not in gleissoll_vocab:
        #print('Fehlt')
        gleissoll_vocab.append(gleissoll)

      # preprocess datum
      datum = str(datum)
      datum = datum.replace("-", "")

      
      # end preprocessing


      # collect preprocessed values and save them
      # Now write the results
      csv_writer.writerow(row) # write records
except Exception as ex:
   print ("Error: unable to fetch data")
   print (ex)

# TODO write/save vocabfile
#zugklasse_vocab
#print(zugklasse_vocab)
writevocalfile('zugklasse',zugklasse_vocab)
writevocalfile('zugowner',zugowner_vocab)
writevocalfile('linie',linie_vocab)
writevocalfile('gleisist',gleisist_vocab)
writevocalfile('gleissoll',gleissoll_vocab)

del csv_writer # close csv file
cursor.close()
mydb.close()
print("Query executed.")
print("Wrote %s rows to csv." % cursor.rowcount)
