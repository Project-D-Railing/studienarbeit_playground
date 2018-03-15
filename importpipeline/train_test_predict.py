import argparse
import shutil
import sys
from glob import glob
import os
import tensorflow as tf

_CSV_COLUMNS = [
    "dailytripid",
    "departuredatestartstation",
    "stopnumber",
    "zugverkehrstyp",
    "zugtyp",
    "zugowner",
    "zugklasse",
    "zugnummer",
    "linie",
    "evanr",
    "arzeitsoll",
    "arzeitist",
    "dpzeitsoll",
    "dpzeitist",
    "gleissoll",
    "gleisist",
    "datum",
    "zugstatus",
    ]

_CSV_COLUMN_DEFAULTS = [[0], [0], [0], [""], [""], [""], [""], [0], [""], [0], [0], [0], [0], [0], [""], [""], [0], [""]]

parser = argparse.ArgumentParser()

parser.add_argument(
    '--model_dir', type=str, default='./model',
    help='Base directory for the model.')

parser.add_argument(
    '--model_type', type=str, default='testa',
    help="Valid model types: {'testa'}.")

parser.add_argument(
    '--train_epochs', type=int, default=400, help='Number of training epochs.')

parser.add_argument(
    '--epochs_per_eval', type=int, default=100,
    help='The number of training epochs to run between evaluations.')

parser.add_argument(
    '--batch_size', type=int, default=1000, help='Number of examples per batch.')

parser.add_argument(
    '--train_data', type=str, default='./train/zuege2_newraw_train.csv',
    help='Path to the training data.')

parser.add_argument(
    '--test_data', type=str, default='./test/zuege2_newraw_test.csv',
    help='Path to the test data.')
parser.add_argument(
    '--predict_data', type=str, default='./predict/zuege2_newraw_test.csv',
    help='Path to the predict data.')


   

   
def build_model_coloumns(model_type):
    id = tf.feature_column.numeric_column('id')
    zugverkehrstyp = tf.feature_column.categorical_column_with_vocabulary_list('zugverkehrstyp', ['D', 'N', 'S', 'F' , 'NULL'])
    arzeitsoll = categorical_column_with_vocabulary_file(key='arzeitsoll', vocabulary_file='./vocabfiles/arzeitsoll.txt',num_oov_buckets=0)

    
    coloumns = [
        id,
        zugverkehrstyp,
        arzeitsoll    
    ]

    return coloumns

def parse_csv(value):
    print('Parsing', value)
    columns = tf.decode_csv(value, record_defaults=_CSV_COLUMN_DEFAULTS)
    features = dict(zip(_CSV_COLUMNS, columns))

    labels = features.pop('arzeitist')
     
    #print(labels)
    #exit()
    return features, labels
    
def input_fn(mode):
    directory = ""
    if mode == "train":
        directory = "./train/*.csv"
    elif mode == "test":
        directory = "./test/*.csv"
    else:
        directory = "./predict/*.csv"
    
    # get all filenames for datasets in this mode, shuffel them
    filenames = glob(os.path.join(directory))
    
    print(filenames)
    #exit()
    filename = filenames[1]
    # Extract lines from input files using the Dataset API.
    dataset = tf.data.TextLineDataset(filenames)
    
    # add shuffle to params
    shuffle = True
    num_epochs = 50
    batch_size = 200
    
    if shuffle:
        dataset = dataset.shuffle(buffer_size=1000)

    dataset = dataset.map(parse_csv, num_parallel_calls=5)

    # We call repeat after shuffling, rather than before, to prevent separate
    # epochs from blending together.
    dataset = dataset.repeat(num_epochs)
    dataset = dataset.batch(batch_size)
 

    return dataset

    
    
def build_estimator(model_dir, model_type):
  """Build an estimator appropriate for the given model type."""

  if model_type == 'testa':
    return tf.estimator.DNNClassifier(
        hidden_units=[100, 75, 50, 25],
        model_dir=model_dir,
        feature_columns=lambda: build_model_coloumns(model_type),
        )
  elif model_type == 'deep':
    return None
  else:
    return None
    
    
    
# MAIN FUNCTION this is the main part
def main(unused_argv):
  # Build out estimator based on our previous saved model and model type
  model = build_estimator(FLAGS.model_dir, FLAGS.model_type)
  print("Model done.")
  # Train and evaluate the model every `FLAGS.epochs_per_eval` epochs.
  for n in range(FLAGS.train_epochs // FLAGS.epochs_per_eval):
    model.train(input_fn=lambda: input_fn('train'))

    #results = model.evaluate(input_fn=lambda: input_fn(
    #    FLAGS.test_data, 1, False, FLAGS.batch_size))

    # Display evaluation metrics
    print('Results at epoch', (n + 1) * FLAGS.epochs_per_eval)
    print('-' * 60)

    #for key in sorted(results):
    #  print('%s: %s' % (key, results[key]))


    
    


if __name__ == '__main__':
  print(tf.__version__)
 # print(dir(tf.feature_column))
  tf.logging.set_verbosity(tf.logging.INFO)
  FLAGS, unparsed = parser.parse_known_args()
  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)