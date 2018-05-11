import sys
import argparse
from glob import glob
import os
import pymysql
import csv
import datetime
import json
import re
import io
import math


parser = argparse.ArgumentParser()

parser.add_argument(
    '--mode', type=str, default='train',
    help='Base mode of execution')

FLAGS, unparsed = parser.parse_known_args()

def timetotimeint(input):
    input = str(input)
    if input == 'None':
     input = "24:00:00"
    hhmmss = input
    (h, m, s) = hhmmss.split(':')
    result = int(h) * 60 + int(m)
    result = math.floor(result/5)
    return result

def openvocalfile(name):
    lines = []
    filename = "./vocabfiles/" + str(name) + ".txt"
    with open(filename, mode="w+", encoding="utf-8") as file:
        for line in file:
            line = line.rstrip('\n')
            lines.append(line)
    return lines    
    
def writevocalfile(name,vocab):
    lines = vocab
    filename = "./vocabfiles/" + str(name) + ".txt"
    with open(filename, mode="w+", encoding="utf-8") as file:
        for item in lines:
            if item == "":
                print("No item found, dont save")
            else:
                file.write("%s\n" % item)
     
# use this funktion to determine which ID's are already selected and used
def lookuplocalfiles():
    files_list = glob(os.path.join('./train', '*.csv'))
    print("Files in train folder:")  
    for a_file in sorted(files_list):
        print(a_file)  

    files_list = glob(os.path.join('./test', '*.csv'))
    print("Files in test folder:")  
    for a_file in sorted(files_list):
        print(a_file)  

    files_list = glob(os.path.join('./predict', '*.csv'))
    print("Files in predict folder:")  
    for a_file in sorted(files_list):
        print(a_file)  


# open config file with database access and some other stuff
with open('config.json', 'r') as f:
    config = json.load(f)
    
# connect to database
mydb = pymysql.connect(config['host'],config['user'],config['password'],config['database'])
cursor = mydb.cursor()

MODE = FLAGS.mode

### write to csv file

if MODE == "predict":
    # prediction files
    query = ("SELECT id, zugid, zugverkehrstyp, zugtyp, zugowner, zugklasse, zugnummer, zugnummerfull, linie, evanr, arzeitsoll, arzeitist, dpzeitsoll, dpzeitist, gleissoll, gleisist, datum, streckengeplanthash, streckenchangedhash, zugstatus FROM zuege WHERE zugklasse='ICE' order by id desc LIMIT 50")
    csv_writer_predict = csv.writer(open("./predict/predict.csv", "wt", newline="\n", encoding="utf-8")) # create csv
    csv_writer_predict_result = csv.writer(open("./predict/predict.txt", "wt", newline="\n", encoding="utf-8")) # create txt for proof
else:
    # train and test files
    query = ("SELECT id, zugid, zugverkehrstyp, zugtyp, zugowner, zugklasse, zugnummer, zugnummerfull, linie, evanr, arzeitsoll, arzeitist, dpzeitsoll, dpzeitist, gleissoll, gleisist, datum, streckengeplanthash, streckenchangedhash, zugstatus FROM zuege WHERE zugklasse='ICE' order by id desc LIMIT 50,50000")
    csv_writer_train = csv.writer(open("./train/train.csv", "wt", newline="\n", encoding="utf-8")) # create csv
    csv_writer_test = csv.writer(open("./test/test.csv", "wt", newline="\n", encoding="utf-8")) # create csv

try:
   cursor.execute(query)
   results = cursor.fetchall()

   zugklasse_vocab = openvocalfile('zugklasse')
   zugowner_vocab = openvocalfile('zugowner')
   linie_vocab = openvocalfile('linie')
   gleisist_vocab = openvocalfile('gleisist')
   gleissoll_vocab = openvocalfile('gleissoll')
   countentrys = 0

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
      #this regex matches zugid into 3 groups
      match = re.match(r"(\-*[0-9]*)\-([0-9]*)\-([0-9]*)$", zugid)
      dailytripid = match.group(1)
      dailytripidparta = dailytripid[:6]
      dailytripidpartb = dailytripid[6:12]
      dailytripidpartc = dailytripid[12:]
      departuredatestartstation = match.group(2)
      stopnumber = match.group(3)
     
      # preprocess times in function
      arzeitsoll = timetotimeint(arzeitsoll)
      arzeitist = timetotimeint(arzeitist)
      dpzeitsoll = timetotimeint(dpzeitsoll)
      dpzeitist = timetotimeint(dpzeitist)
      
      # preprocess zugowner
      if zugowner not in zugowner_vocab:
        zugowner_vocab.append(zugowner)
      
      # preprocess zugklasse
      if zugklasse not in zugklasse_vocab:
        zugklasse_vocab.append(zugklasse)

      # preprocess linie
      if linie not in linie_vocab:
        linie_vocab.append(linie)

      # preprocess gleisist,gleissoll
      if gleisist not in gleisist_vocab:
        gleisist_vocab.append(gleisist)

      if gleissoll not in gleissoll_vocab:
        gleissoll_vocab.append(gleissoll)

      # preprocess datum
      datum = str(datum)
      datum = datum.replace("-", "")

      empty = None
      # end preprocessing

      row = []
      row_proof = []
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
      if MODE == "predict":
        row.append(empty)
        row_proof.append(linie)
      else:
        row.append(linie)
      row.append(evanr)
      row.append(arzeitsoll)
      if MODE == "predict":
        row.append(empty)
        row_proof.append(arzeitist)
      else:
        row.append(arzeitist)
      row.append(dpzeitsoll)
      if MODE == "predict":
        row.append(empty)
        row_proof.append(dpzeitist)
      else:
        row.append(dpzeitist)
      row.append(gleissoll)
      if MODE == "predict":
        row.append(empty)
        row_proof.append(gleisist)
      else:
        row.append(gleisist)
      row.append(datum)
      if MODE == "predict":
        row.append(empty)
        row_proof.append(zugstatus)
      else:
        row.append(zugstatus)
      # collect preprocessed values and save them
      # write the results
      if MODE == "predict":
        #write row to predict file
        csv_writer_predict.writerow(row)
        csv_writer_predict_result.writerow(row_proof)
      else:
        if (countentrys % 10 == 1):
            #write row to test file
            csv_writer_test.writerow(row)
        else:
            #write row to train file
            csv_writer_train.writerow(row)

        countentrys = countentrys + 1
except Exception as ex:
   print ("Error: unable to fetch data")
   print (ex)

# writing vocabfiles
writevocalfile('zugklasse',zugklasse_vocab)
writevocalfile('zugowner',zugowner_vocab)
writevocalfile('linie',linie_vocab)
writevocalfile('gleisist',gleisist_vocab)
writevocalfile('gleissoll',gleissoll_vocab)
try:
    del csv_writer_train # close csv file
    del csv_writer_test # close csv file
except Exception as ex:
    #none
    print("Ignore: no file writer for test or train")
try:
    del csv_writer_predict # close csv file
    del csv_writer_predict_result # close proof file
except Exception as ex:
    #none
    print("Ignore: no file writer for predict")

cursor.close()
mydb.close()
print("Query executed.")
print("Wrote %s rows to csv." % cursor.rowcount)
#list all generated files
lookuplocalfiles()
