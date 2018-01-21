import tensorflow as tf

# Model parameters
W = tf.Variable([.3], dtype=tf.float32)
b = tf.Variable([-.3], dtype=tf.float32)
A = tf.Variable([-.3], dtype=tf.float32)
# Model input and output
x = tf.placeholder(tf.float32)
linear_model = W*x + b
y = tf.placeholder(tf.float32)

# loss
loss = tf.reduce_sum(tf.square(linear_model - y)) # sum of the squares
# optimizer
optimizer = tf.train.GradientDescentOptimizer(0.01)
train = optimizer.minimize(loss)

# training data
x_train = [1, 2, 3, 4]
y_train = [-3, -2, -1, 0]
# training loop
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init) # reset values to wrong
for i in range(10000):
  sess.run(train, {x: x_train, y: y_train})

# evaluate training accuracy
curr_A, curr_W, curr_b, curr_loss = sess.run([A, W, b, loss], {x: x_train, y: y_train})
print("A: %s W: %s b: %s loss: %s"%(curr_A, curr_W, curr_b, curr_loss))
