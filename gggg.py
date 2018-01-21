"""Sample TensorFlow benchmark."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time

import tensorflow as tf


# Define a class that extends from tf.test.Benchmark.
class SampleBenchmark(tf.test.Benchmark):

  # Note: benchmark method name must start with `benchmark`.
  def benchmarkSum(self):
    with tf.Session() as sess:
      x = tf.constant(10)
      y = tf.constant(5)
      result = tf.add(x, y)

      iters = 100
      start_time = time.time()
      for i in range(iters):
        sess.run(result)
      total_wall_time = time.time() - start_time

      # Call report_benchmark to report a metric value.
      self.report_benchmark(
          name="sum_wall_time",
          # This value should always be per iteration.
          wall_time=total_wall_time/iters,
          iters=iters)


tf.test.main()
