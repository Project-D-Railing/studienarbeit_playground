# Steps

* Read data of MySQL Database
* Format data and do some error correction stuff
* Extract feature distinct values (for .txt vocab files)
* write data to .csv
* Read data for tensorflow based on .csv and .txt files
* ????
* Profit!!!

# TODO

* Autoprocess and detect existing files
* Split train and test datasets here and generate new one if wanted by user/model
* Make triple input_fn possible for training, testing and predicting
* Generate acustom estimator and use input_fn from other models and rewrite input pipe
* Make predictions possible to see if everything is alright with our features
* Remove unknown or useless feature to shrink datasets and size
* Generate structure for model savepoints based on estimator settings (e.g. different hidden layer values,...)


# IDEA

* the predictions are processed like datasets from a table and generated to csv files. These files are predicted and the results are passed back to the database.
