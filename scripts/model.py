import tensorflow as tf
# from tensorflow.keras import layers
# from tensorflow.keras import Model
# from tensorflow.keras import models

# from tensorflow import keras
# import tensorflow.keras.models
# from keras.layers import Conv1D

def base_cnn(vector_size):
    """
    Builds a base CNN with provided vector_size
    :param vector_size:
    :return: base CNN (tf.keras.Model)
    """
    # input layer
    inputs = tf.keras.Input(shape=(vector_size,))

    # layers
    dense1 = tf.keras.layers.Dense(64, activation="relu")(inputs)

    # outputs
    outputs = tf.keras.layers.Dense(10)(dense1)

    # base CNN model
    base_cnn_model = tf.keras.Model(inputs=inputs, outputs=outputs, name="base_cnn")

    return base_cnn_model

class DistanceLayer(tf.keras.layers.Layer):
    """
    Computes distance between two vectors with simple euclidean distance
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def call(self, sample1, sample2):
        distance = tf.reduce_sum(tf.norm(sample1-sample2, ord='euclidean'))
        return distance