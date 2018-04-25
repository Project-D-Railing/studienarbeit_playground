import argparse
import shutil
import sys
from glob import glob
import os
import tensorflow as tf
import matplotlib.pyplot as plt

_CSV_COLUMNS = [
    "dailytripidparta",
    "dailytripidpartb",
    "dailytripidpartc",
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

_CSV_COLUMN_DEFAULTS = [[0], [0], [0], [0], [0], [""], [""], [""], [""], [0], [""], [0], [0], [0], [0], [0], [""], [""], [0], [""]]

parser = argparse.ArgumentParser()

parser.add_argument(
    '--model_dir', type=str, default='./model',
    help='Base directory for the model.')

parser.add_argument(
    '--model_type', type=str, default='testa',
    help="Valid model types: {'testa'}.")

parser.add_argument(
    '--train_epochs', type=int, default=3000, help='Number of training epochs.')

parser.add_argument(
    '--epochs_per_eval', type=int, default=2,
    help='The number of training epochs to run between evaluations.')

parser.add_argument(
    '--batch_size', type=int, default=1000, help='Number of examples per batch.')

parser.add_argument(
    '--train_data', type=str, default='./train/CSV_Output.csv',
    help='Path to the training data.')

parser.add_argument(
    '--test_data', type=str, default='./test/CSV_Output.csv',
    help='Path to the test data.')
parser.add_argument(
    '--predict_data', type=str, default='./predict/zuege2_newraw_test.csv',
    help='Path to the predict data.')


   

   
def build_model_coloumns(model_type):
    if model_type == "testa":
        dailytripidparta = tf.feature_column.numeric_column('dailytripidparta')
        dailytripidpartb = tf.feature_column.numeric_column('dailytripidpartb')
        dailytripidpartc = tf.feature_column.numeric_column('dailytripidpartc')
        departuredatestartstation = tf.feature_column.numeric_column('departuredatestartstation')
        stopnumber = tf.feature_column.numeric_column('stopnumber')
        zugverkehrstyp = tf.feature_column.indicator_column(tf.feature_column.categorical_column_with_vocabulary_list('zugverkehrstyp', ['D', 'N', 'S', 'F' , 'NULL']))
        zugtyp = tf.feature_column.indicator_column(tf.feature_column.categorical_column_with_vocabulary_list('zugtyp', ['p', 'NULL']))
        zugowner = tf.feature_column.indicator_column(tf.feature_column.categorical_column_with_vocabulary_file(key='zugowner', vocabulary_file='./vocabfiles/zugowner.txt',num_oov_buckets=10))
        zugklasse = tf.feature_column.indicator_column(tf.feature_column.categorical_column_with_vocabulary_file(key='zugklasse', vocabulary_file='./vocabfiles/zugklasse.txt',num_oov_buckets=10))
        zugnummer = tf.feature_column.numeric_column('zugnummer')
        #linie = tf.feature_column.numeric_column('linie')
        evanr = tf.feature_column.numeric_column('evanr')
        arzeitsoll = tf.feature_column.numeric_column('arzeitsoll')
        #arzeitist = tf.feature_column.numeric_column('arzeitist')
        dpzeitsoll = tf.feature_column.numeric_column('dpzeitsoll')
        #dpzeitist = tf.feature_column.numeric_column('dpzeitist')
        gleissoll = tf.feature_column.indicator_column(tf.feature_column.categorical_column_with_vocabulary_file(key='gleissoll', vocabulary_file='./vocabfiles/gleissoll.txt',num_oov_buckets=10))
        #gleisist = tf.feature_column.indicator_column(tf.feature_column.categorical_column_with_vocabulary_file(key='gleisist', vocabulary_file='./vocabfiles/gleisist.txt',num_oov_buckets=10))
        datum = tf.feature_column.numeric_column('datum')
        #zugstatus = tf.feature_column.indicator_column(tf.feature_column.categorical_column_with_vocabulary_list('zugstatus', ['n', 'c', 'p']))
        
        coloumns = [
            dailytripidparta,
            dailytripidpartb,
            dailytripidpartc,
            departuredatestartstation,
            stopnumber,
            zugverkehrstyp,
            zugtyp,
            zugowner,
            zugklasse,
            zugnummer,
            #linie,
            evanr,
            arzeitsoll,
            #arzeitist,
            dpzeitsoll,
            #dpzeitist,
            gleissoll,
            #gleisist,
            datum,
            #zugstatus,    
        ]
    else:
        coloumns = None

    return coloumns

def parse_csv(value):
    print('Parsing', value)
    columns = tf.decode_csv(value, record_defaults=_CSV_COLUMN_DEFAULTS)
    features = dict(zip(_CSV_COLUMNS, columns))
    #none = features.pop('dpzeitist')
    #none2 = features.pop('gleisist')
    labels = features.pop('arzeitist')
    

    return features, labels
    
def input_fn_mode(mode):
    filenames = ""
    if mode == "train":
        filenames = glob(os.path.join('./train', '*.csv'))
    elif mode == "test":
        filenames = glob(os.path.join('./test', '*.csv'))
    else:
        filenames = glob(os.path.join('./predict', '*.csv'))
    
    # get all filenames for datasets in this mode, shuffel them

   # filename = filenames[0]
    #print(filenames)
    #exit()

   
    filename = filenames[0]
    # Extract lines from input files using the Dataset API.
    dataset = tf.data.TextLineDataset(filename)
    print(filename)
    #exit()
    # add shuffle to params
    shuffle = True
    num_epochs = 4000
    batch_size = 1
    
    if shuffle:
        dataset = dataset.shuffle(buffer_size=100000)

    dataset = dataset.map(parse_csv, num_parallel_calls=5)

    # We call repeat after shuffling, rather than before, to prevent separate
    # epochs from blending together.
    dataset = dataset.repeat(num_epochs)
    dataset = dataset.batch(batch_size)
 
    #print(dataset)
    #exit()
    return dataset

    
    
def build_estimator(model_dir, model_type):

  base_coloumns = build_model_coloumns('testa')
  """Build an estimator appropriate for the given model type."""
  learning_rate = 0.02
  if model_type == 'testa':
    #optimizer = tf.train.FtrlOptimizer(learning_rate=learning_rate, l2_regularization_strength=0.000)
    optimizer = tf.train.ProximalAdagradOptimizer(learning_rate=learning_rate,initial_accumulator_value=0.1,l1_regularization_strength=0.0,l2_regularization_strength=0.0,use_locking=False,name='ProximalAdagrad')
    return tf.estimator.DNNClassifier(
        hidden_units=[40,40],
        model_dir=model_dir,
        feature_columns=base_coloumns,
        optimizer=optimizer,
        activation_fn=tf.nn.relu,
        dropout=0.0,
        loss_reduction=tf.losses.Reduction.MEAN,
        n_classes=1441)
  elif model_type == 'deep':
    return None
  else:
    optimizer = tf.train.FtrlOptimizer(learning_rate=50.0, l2_regularization_strength=0.1)

    estimator = tf.contrib.kernel_methods.KernelLinearClassifier(
        n_classes=1441, optimizer=optimizer)

  
  
    return None
    
    
    
# MAIN FUNCTION this is the main part
def main(unused_argv):
  # Clean up the model directory if present
  #shutil.rmtree(FLAGS.model_dir, ignore_errors=True)

  model = build_estimator(FLAGS.model_dir, FLAGS.model_type)
  print("Model done.")
  # Train and evaluate the model every `FLAGS.epochs_per_eval` epochs.
  for n in range(FLAGS.train_epochs // FLAGS.epochs_per_eval):
    model.train(input_fn=lambda: input_fn_mode("train"),steps=5000)

    results = model.evaluate(input_fn=lambda: input_fn_mode("test"),steps=10)
    
    predictions = model.predict(input_fn=lambda: input_fn_mode("predict"))
    
    for pred_dict in zip(predictions):
    

        print(pred_dict[0]['probabilities'])
        print(pred_dict[0]['class_ids'][0])
        plt.plot(pred_dict[0]['probabilities'])
        plt.ylabel('some numbers')
        #plt.show()
        break
        

    # Display evaluation metrics
    print('Results at epoch', (n + 1) * FLAGS.epochs_per_eval)
    print('-' * 60)

    for key in sorted(results):
      print('%s: %s' % (key, results[key]))



    
    


if __name__ == '__main__':
  print(tf.__version__)
 # print(dir(tf.feature_column))
  tf.logging.set_verbosity(tf.logging.INFO)
  FLAGS, unparsed = parser.parse_known_args()
  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
