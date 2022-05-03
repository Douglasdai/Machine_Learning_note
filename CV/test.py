import torch
import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
print(tf.reduce_sum(tf.random.normal([1000, 1000])))
# mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)

# # Load data
# X_train = mnist.train.images
# Y_train = mnist.train.labels
# X_test = mnist.test.images
# Y_test = mnist.test.labels
# batch_X, batch_Y = mnist.train.next_batch(64)
# print(batch_X)
