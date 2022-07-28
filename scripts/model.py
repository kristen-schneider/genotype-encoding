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
    inputs = tf.keras.Input(shape=(vector_size, 1))

    # layers
    x = tf.keras.layers.Conv1d(filters=6, kernal_size=3, activation="relu")(inputs)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Conv1d(filters=6, kernal_size=3, activation="relu")(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.GlobalAveragePooling1D()(x)
    # dense1 = tf.keras.layers.Dense(40, activation="relu", name="one")(inputs)
    # dense2 = tf.keras.layers.Dense(20, activation="relu", name="two")(dense1)

    # outputs
    outputs = tf.keras.layers.Conv1d(filters=6, kernal_size=3, activation="relu")(x)

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
        distance = tf.reduce_sum(tf.norm(sample1 - sample2, ord='euclidean'))
        return distance

class SiameseModel(tf.keras.Model):
    """
    Computes loss using two embeddings proces by base CNN
    """
    def __init__(self, siamese_network):
        super(SiameseModel, self).__init__()
        self.siamese_network = siamese_network
        self.loss_tracker = tf.keras.metrics.Mean(name="loss")

    def call(self, data):
        sample1, sample2 = data[:2]
        sample1 = tf.expand_dims(input=sample1, axis=-1)
        sample2 = tf.expand_dims(input=sample2, axis=-1)

        return self.siamese_network(tf.expand_dims(input=sample1, axis=-1),
                                    tf.expand_dims(input=sample2, axis=-1))

    def train_step(self, data):
        """
        :param data: sample1, sample2
        :return:
        """
        sample_data = data[:2]
        target_data = data[2]

        with tf.GradientTape() as tape:
            loss = self._compute_loss(sample_data, target_data)

        gradients = tape.gradient(loss, self.siamese_network.trainable_weights)

        self.optimizer.apply_gradients(
            zip(gradients, self.siamese_network.trainable_weights)
        )

        self.loss_tracker.update_state(loss)
        return {"loss": self.loss_tracker.result()}

    def test_step(self, data):
        loss = self._compute_loss(data)

        self.loss_tracker.update_state(loss)
        return {"loss": self.loss_tracker.result()}

    def _compute_loss(self, sample_data, target_distances):
        print(self.siamese_network.summary())
        predicted_distance = self.siamese_network(sample_data)
        loss = tf.keras.metrics.mean_squared_error(
            predicted_distance, target_distances
        )
        return loss

    @property
    def metrics(self):
        return [self.loss_tracker]
