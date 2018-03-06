import tensorflow as tf
def input_fn_train():
    directory = "./train/*.csv"
    filename_queue = tf.train.string_input_producer(
        tf.train.match_filenames_once(directory),
        shuffle=True)

    # Each file will have a header, we skip it and give defaults and type information
    # for each column below.
    line_reader = tf.TextLineReader(skip_header_lines=1)

    _, csv_row = line_reader.read(filename_queue)

    # Type information and column names based on the decoded CSV.
    record_defaults = [[""], [""], [""], [""], [""], [""], [""], [""], [""], [""], [""], [""], [""], [""], [""], [""], [""], [""], [""], [""]]
    id, zugid, zugverkehrstyp, zugtyp, zugowner, zugklasse, zugnummer, zugnummerfull, linie, evanr, arzeitsoll, arzeitist, dpzeitsoll, dpzeitist, gleissoll, gleisist, datum, streckengeplanthash, streckenchangedhash, zugstatus = \
        tf.decode_csv(csv_row, record_defaults=record_defaults)

    # Turn the features back into a tensor.
    features = tf.stack([
        id,
        zugid,
        zugverkehrstyp,
        zugtyp,
        zugowner,
        zugklasse,
        zugnummer,
        zugnummerfull,
        linie,
        evanr,
        arzeitsoll,
        arzeitist,
        dpzeitsoll,
        dpzeitist,
        gleissoll,
        gleisist,
        datum,
        streckengeplanthash,
        streckenchangedhash,
        zugstatus])
    return features 

    


    
    
with tf.Session() as sess:
    print("OK")
    

    # Estimator using the default optimizer.
    estimator = tf.contrib.learn.LinearClassifier(feature_columns=features)

    estimator.train(input_fn=input_fn_train)
    estimator.evaluate(input_fn=input_fn_train)
    estimator.predict(input_fn=input_fn_train)

    
