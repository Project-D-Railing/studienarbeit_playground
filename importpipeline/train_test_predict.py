import argparse
import shutil
import sys

import tensorflow as tf


_CSV_COLUMNS = [
    "id", "zugid", "zugverkehrstyp", "zugtyp", "zugowner", "zugklasse", "zugnummer", "zugnummerfull", "linie", "evanr", "arzeitsoll", "arzeitist", "dpzeitsoll", "dpzeitist", "gleissoll", "gleisist", "datum", "streckengeplanthash", "streckenchangedhash", "zugstatus"
]

_CSV_COLUMN_DEFAULTS = [[0], [""], [""], [""], [""], [""], [0], [""], [""], [0], [""], [""], [""], [""], [""], [""], [""], [""], [""], [""]]

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

    
def build_estimator(model_dir, model_type):
  """Build an estimator appropriate for the given model type."""

  if model_type == 'testa':
    return tf.estimator.DNNClassifier(
        hidden_units=[100, 75, 50, 25],
        model_dir=model_dir,
        feature_columns=lambda: build_model_coloumns(model_type),
        )
  elif model_type == 'deep':
    
  else:
    
    
    
# MAIN FUNCTION this is the main part
def main(unused_argv):
  # Build out estimator based on our previous saved model and model type
  model = build_estimator(FLAGS.model_dir, FLAGS.model_type)
  print("Model done.")
  # Train and evaluate the model every `FLAGS.epochs_per_eval` epochs.
  for n in range(FLAGS.train_epochs // FLAGS.epochs_per_eval):
    model.train(input_fn=lambda: input_fn(
        FLAGS.train_data, FLAGS.epochs_per_eval, True, FLAGS.batch_size))

    results = model.evaluate(input_fn=lambda: input_fn(
        FLAGS.test_data, 1, False, FLAGS.batch_size))

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