import tensorflow as tf
import os


print("Import completed")
print("Starting up Model")



def lol(x,y):
 return x+y

def create_file_reader_ops(filename_queue):
    reader = tf.TextLineReader(skip_header_lines=1)
    _, csv_row = reader.read(filename_queue)
    record_defaults = [[""], [""], [0], [0], [0], [0]]
    country, code, gold, silver, bronze, total = tf.decode_csv(csv_row, record_defaults=record_defaults)
    features = tf.pack([gold, silver, bronze])
    return features, country


#print(lol(18,24))



dir_path = os.path.dirname(os.path.realpath(__file__))
filename = dir_path + "/testdata.csv"

features = tf.placeholder(tf.int32, shape=[3], name='features')
country = tf.placeholder(tf.string, name='country')
total = tf.reduce_sum(features, name='total')



with tf.Session() as sess:
    sess.run( tf.global_variables_initializer())
    with open(filename) as inf:
        # Skip header
        next(inf)
        for line in inf:
            # Read data, using python, into our features
            country_name, code, gold, silver, bronze, total = line.strip().split(",")
            gold = int(gold)
            silver = int(silver)
            bronze = int(bronze)
            # Run the Print ob
           # printerop = tf.Print(total, [country, features, total], name='printer')
          #  total = sess.run(printerop, feed_dict={features: [gold, silver, bronze], country:country_name})
            
            print(country_name, bronze, silver, gold ,total)




print("Stopping now")
