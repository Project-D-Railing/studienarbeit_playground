# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Example code for TensorFlow Wide & Deep Tutorial using tf.estimator API."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

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
    '--model_dir', type=str, default='/home/dominikschmitt/Dokumente/Github/studienarbeit_playground/wide_deep/model',
    help='Base directory for the model.')

parser.add_argument(
    '--model_type', type=str, default='wide_deep',
    help="Valid model types: {'wide', 'deep', 'wide_deep'}.")

parser.add_argument(
    '--train_epochs', type=int, default=400, help='Number of training epochs.')

parser.add_argument(
    '--epochs_per_eval', type=int, default=100,
    help='The number of training epochs to run between evaluations.')

parser.add_argument(
    '--batch_size', type=int, default=1000, help='Number of examples per batch.')

parser.add_argument(
    '--train_data', type=str, default='/home/dominikschmitt/Dokumente/Github/studienarbeit_playground/wide_deep/zuege2_newraw_train.csv',
    help='Path to the training data.')

parser.add_argument(
    '--test_data', type=str, default='/home/dominikschmitt/Dokumente/Github/studienarbeit_playground/wide_deep/zuege2_newraw_test.csv',
    help='Path to the test data.')

_NUM_EXAMPLES = {
    'train': 8000,
    'validation': 1000,
}


def build_model_columns():
  """Builds a set of wide and deep feature columns."""
  # Continuous columns
  id = tf.feature_column.numeric_column('id')
 # zugid = tf.feature_column.categorical_column_with_hash_bucket('zugid', hash_bucket_size=1000000000)
  zugverkehrstyp = tf.feature_column.categorical_column_with_vocabulary_list('zugverkehrstyp', ['D', 'N', 'S', 'F' , 'NULL'])
  zugtyp = tf.feature_column.categorical_column_with_vocabulary_list('zugtyp', ['p', 'NULL'])
  zugowner = tf.feature_column.categorical_column_with_hash_bucket('zugowner', hash_bucket_size=1000)
  zugklasse = tf.feature_column.categorical_column_with_hash_bucket('zugklasse', hash_bucket_size=1000)
  zugnummer = tf.feature_column.numeric_column('zugnummer')
 # zugnummerfull = tf.feature_column.categorical_column_with_hash_bucket('zugnummerfull', hash_bucket_size=10000000)
  linie = tf.feature_column.categorical_column_with_hash_bucket('linie', hash_bucket_size=1000)
  evanr = tf.feature_column.numeric_column('evanr')
 # arzeitsoll = tf.feature_column.categorical_column_with_hash_bucket('arzeitsoll', hash_bucket_size=2000)
 # arzeitist = tf.feature_column.categorical_column_with_hash_bucket('arzeitist', hash_bucket_size=2000)
  dpzeitsoll = tf.feature_column.categorical_column_with_hash_bucket('dpzeitsoll', hash_bucket_size=2000)
  dpzeitist = tf.feature_column.categorical_column_with_hash_bucket('dpzeitist', hash_bucket_size=2000)
  gleissoll = tf.feature_column.categorical_column_with_hash_bucket('gleissoll', hash_bucket_size=2000)
  gleisist = tf.feature_column.categorical_column_with_hash_bucket('gleisist', hash_bucket_size=2000)
  datum = tf.feature_column.categorical_column_with_hash_bucket('datum', hash_bucket_size=2000)
 # streckengeplanthash = tf.feature_column.categorical_column_with_hash_bucket('streckengeplanthash', hash_bucket_size=2000000)
 # streckenchangedhash = tf.feature_column.categorical_column_with_hash_bucket('streckenchangedhash', hash_bucket_size=2000000)
  zugstatus = tf.feature_column.categorical_column_with_vocabulary_list('zugstatus', ['n', 'c', 'p'])


  # Transformations.
#  age_buckets = tf.feature_column.bucketized_column(
#      age, boundaries=[18, 25, 30, 35, 40, 45, 50, 55, 60, 65])

  # Wide columns and deep columns.
  base_columns = [
      id,
  #    zugid,
      zugverkehrstyp,
      zugtyp,
      zugowner,
      zugklasse,
      zugnummer,
  #    zugnummerfull,
      linie,
      evanr,
  #   arzeitsoll,
  #    arzeitist,
      dpzeitsoll,
      dpzeitist,
      gleissoll,
      gleisist,
      datum,
   #   streckengeplanthash,
  #    streckenchangedhash,
      zugstatus
  ]

 # crossed_columns = [
 #      tf.feature_column.crossed_column(
 #         ['education', 'occupation'], hash_bucket_size=1000),
 #     tf.feature_column.crossed_column(
 #         [age_buckets, 'education', 'occupation'], hash_bucket_size=1000),
 # ]

  wide_columns = base_columns # + crossed_columns

  deep_columns = [
  #    id,
  #    zugnummer
      ]

  return wide_columns, deep_columns


def build_estimator(model_dir, model_type):
  """Build an estimator appropriate for the given model type."""
  wide_columns, deep_columns = build_model_columns()
  hidden_units = [100, 75, 50, 25]

  # Create a tf.estimator.RunConfig to ensure the model is run on CPU, which
  # trains faster than GPU for this model.
  run_config = tf.estimator.RunConfig() #.replace(
  #    session_config=tf.ConfigProto(device_count={'GPU': 0}))

  if model_type == 'wide':
    return tf.estimator.LinearClassifier(
        model_dir=model_dir,
        feature_columns=wide_columns,
        config=run_config)
  elif model_type == 'deep':
    return tf.estimator.DNNClassifier(
        model_dir=model_dir,
        feature_columns=deep_columns,
        hidden_units=hidden_units,
        config=run_config)
  else:
    return tf.estimator.DNNLinearCombinedClassifier(
        model_dir=model_dir,
        linear_feature_columns=wide_columns,
        dnn_feature_columns=deep_columns,
        dnn_hidden_units=hidden_units,
        config=run_config)


def input_fn(data_file, num_epochs, shuffle, batch_size):
  """Generate an input function for the Estimator."""
  assert tf.gfile.Exists(data_file), (
      '%s not found. Please make sure you have either run data_download.py or '
      'set both arguments --train_data and --test_data.' % data_file)

  def parse_csv(value):
    print('Parsing', data_file)
    columns = tf.decode_csv(value, record_defaults=_CSV_COLUMN_DEFAULTS)
    features = dict(zip(_CSV_COLUMNS, columns))
    labels = features.pop('arzeitist')
    #print(labels)
    #exit()
    labels = tf.equal(labels, features.pop('arzeitsoll'))
    return features, labels

  # Extract lines from input files using the Dataset API.
  dataset = tf.data.TextLineDataset(data_file)

  if shuffle:
    dataset = dataset.shuffle(buffer_size=_NUM_EXAMPLES['train'])

  dataset = dataset.map(parse_csv, num_parallel_calls=5)

  # We call repeat after shuffling, rather than before, to prevent separate
  # epochs from blending together.
  dataset = dataset.repeat(num_epochs)
  dataset = dataset.batch(batch_size)
  return dataset


def main(unused_argv):
  # Clean up the model directory if present
  shutil.rmtree(FLAGS.model_dir, ignore_errors=True)
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
