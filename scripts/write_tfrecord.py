import tensorflow as tf

import utils

# code snippits from: https://www.tensorflow.org/tutorials/load_data/tfrecord

def to_tfrecord(dataset):
    """

    :param dataset: tf dataset with s1, s2, distances
    :return: write to tf record
    """
    # .take(1) is taking 1 batch
    for s1, s2, distances in dataset.take(1):
        print(s1)
        print(s2)
        print(distances)
        tf_serialize_example(s1, s2, distances)

def tf_serialize_example(s1, s2, distances):
  tf_string = tf.py_function(
    serialize_example,
    (s1, s2, distances),  # Pass these args to the above function.
    tf.string)      # The return type is `tf.string`.
  return tf.reshape(tf_string, ()) # The result is a scalar.

def serialize_example(sample1, sample2, distances):
  """
  Creates a tf.train.Example message ready to be written to a file.
  """
  # Create a dictionary mapping the feature name to the tf.train.Example-compatible
  # data type.
  feature = {
      'sample1': utils._int64_feature(sample1),
      'sample2': utils._int64_feature(sample2),
      'distances': utils._float_feature(distances),
  }

  # Create a Features message using tf.train.Example.

  example_proto = tf.train.Example(features=tf.train.Features(feature=feature))
  return example_proto.SerializeToString()
