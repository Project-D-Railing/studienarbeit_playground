import sys
from glob import glob
import os
import pymysql
import csv
import datetime
import json
import re
import io

# used by arzeitist,arzeitsoll,dpzeitist,dpzeitsoll
def timetotimeint(input):
    input = str(input)
    # first check all times if they are none
    if input == 'None':
     input = "24:00:00"
       
    # now all times are 'valid' ehhrrmmm
    # convert tome to integer none values are now negative numbers like -1
    hhmmss = input
    (h, m, s) = hhmmss.split(':')
    result = int(h) * 60 + int(m)
    return result

    
#used instead of hash buckets to get a better idea of the meaing of the values  
#warning this function is slow
def coloumntovocalfileold(name,input):
    # ii#
    filename = "./vocabfiles/" + str(name) + ".txt"
    with io.open(filename, mode="r+", encoding="utf-8") as file:
        for line in file:
            if input in line:
                break
        else: # not found, we are at the eof
            file.write(input) # append missing data
    

def openvocalfile(name):
    # ii#
    lines = []
    filename = "./vocabfiles/" + str(name) + ".txt"
    with open(filename, mode="w+", encoding="utf-8") as file:
        for line in file:
            line = line.rstrip('\n')
            lines.append(line)
    return lines    
    
def writevocalfile(name,vocab):
    # ii#
    lines = vocab
    filename = "./vocabfiles/" + str(name) + ".txt"
    with open(filename, mode="w+", encoding="utf-8") as file:
        for item in lines:
            if item == "":
                print("None item found, dont save")
            else:
                file.write("%s\n" % item)
     
# use this funktion to determine which ID's are already selected and used
def lookuplocalfiles():
    files_list = glob(os.path.join('./train', '*.csv'))
    for a_file in sorted(files_list):
        print(a_file)  
  


# open config file with database access and some other stuff
with open('config.json', 'r') as f:
    config = json.load(f)
    # pack these as parameters or into a config file
    MODE = 'train'
    STARTID = 1000000
    ENDID = 1250000
# TODO create functions for query and parsing and preprocessing and write to csv    
    
# connect to database
mydb = pymysql.connect(config['host'],config['user'],config['password'],config['database'])
cursor = mydb.cursor()

## query
query = ("SELECT * FROM zuege2 WHERE id > '%s' AND id < '%s' LIMIT 500000")


### write to csv file

# Generate switch by mode and int of entries per file
# e.g.  test, 1000
# or    train, 20000
# for predict use other db with entries which should be predicted coming from a web interface or other tool
csv_writer = csv.writer(open("./train/CSV_Output.csv", "wt", newline="\n", encoding="utf-8")) # create csv
try:
   # Execute the SQL command
   cursor.execute(query,[STARTID,ENDID])
   # Fetch all the rows in a list of lists.
   results = cursor.fetchall()
  
   # this are the headers of the database but we customize these
   #csv_writer.writerow([i[0] for i in cursor.description]) # write headers
   
   zugklasse_vocab = openvocalfile('zugklasse')
   zugowner_vocab = openvocalfile('zugowner')
   linie_vocab = openvocalfile('linie')
   gleisist_vocab = openvocalfile('gleisist')
   gleissoll_vocab = openvocalfile('gleissoll')

   #print(zugklasse_vocab)
   for row in results:
      # ACHTUNG die id ist nicht relevant und sollte nicht mit ins Modell gegeben werden da auto increment aus der Datenbank
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
      dailytripid = match.group(1)
      dailytripidparta = dailytripid[:6]
      dailytripidpartb = dailytripid[6:12]
      dailytripidpartc = dailytripid[12:]
      departuredatestartstation = match.group(2)
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
      row = []
      row.append(dailytripidparta)
      row.append(dailytripidpartb)
      row.append(dailytripidpartc)
      row.append(departuredatestartstation)
      row.append(stopnumber)
      row.append(zugverkehrstyp)
      row.append(zugtyp)
      row.append(zugowner)
      row.append(zugklasse)
      row.append(zugnummer)
      row.append(linie)
      row.append(evanr)
      row.append(arzeitsoll)
      row.append(arzeitist)
      row.append(dpzeitsoll)
      row.append(dpzeitist)
      row.append(gleissoll)
      row.append(gleisist)
      row.append(datum)
      row.append(zugstatus)
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
lookuplocalfiles()
