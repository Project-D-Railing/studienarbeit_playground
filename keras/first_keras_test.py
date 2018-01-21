from keras.models import Sequential
from keras.layers import Dense
from keras.utils import plot_model
import numpy
from keras import backend as K
print(K.tensorflow_backend._get_available_gpus())
# fix random seed for reproducibility
numpy.random.seed(7)

# load dataset
dataset = numpy.genfromtxt('test.csv', delimiter=',', dtype=object)
#print(dataset)


# split into input (X) and output (Y) variables
#print(dataset[:,0])
X = dataset[:,0:8]
Y = dataset[:,8]
#print(X)


print("ok")
# create model
model = Sequential()
model.add(Dense(25600, input_dim=8, activation='relu'))
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='elu'))
model.add(Dense(32, activation='elu'))
model.add(Dense(1, activation='sigmoid'))

# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Fit the model
model.fit(X, Y, epochs=3000, batch_size=1000, verbose=2)

# evaluate the model
scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))


#predictions = model.predict(X)
# round predictions
#rounded = [numpy.round(x) for x in predictions]
#print(rounded)

