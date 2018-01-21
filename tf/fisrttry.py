import tensorflow as tf

directory = "./train/*.csv"
filename_queue = tf.train.string_input_producer(
    tf.train.match_filenames_once(directory),
    shuffle=True)

# Each file will have a header, we skip it and give defaults and type information
# for each column below.
line_reader = tf.TextLineReader(skip_header_lines=1)

_, csv_row = line_reader.read(filename_queue)

# Type information and column names based on the decoded CSV.
record_defaults = [[0.0], [0.0], [0.0], [0.0], [""]]
sepal_length, sepal_width, petal_length, petal_width, iris_species = \
    tf.decode_csv(csv_row, record_defaults=record_defaults)

# Turn the features back into a tensor.
features = tf.stack([
    sepal_length,
    sepal_width,
    petal_length,
    petal_width])

with tf.Session() as sess:
    print("OK")
    print(features)
