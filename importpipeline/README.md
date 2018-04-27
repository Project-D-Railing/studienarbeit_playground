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
* Make predictions possible to see if everything is alright with our features
 (this todo seems to be a problem)
* Remove unknown or useless feature to shrink datasets and size (this is needed in case of a faster prediction testing)
* Generate structure for model savepoints based on estimator settings (e.g. different hidden layer values,...) (this is not needed just ignore or delete unwanted results)


# IDEA

* the predictions are processed like datasets from a table and generated to csv files. These files are predicted and the results are passed back to the database.
