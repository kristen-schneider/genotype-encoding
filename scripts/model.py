import tensorflow as tf
from tensorflow import keras
import keras.models
from keras import layers
from keras.layers import Conv1D

def functional_model(vector_size):
    inputs = keras.Input(shape=(vector_size,))
    dense = layers.Dense(64, activation="relu")
    x = dense(inputs)
    x = layers.Dense(64, activation="relu")(x)
    outputs = layers.Dense(10)(x)
    model = keras.Model(inputs=inputs, outputs=outputs, name="encoding_model")
    model.summary()
    # keras.utils.plot_model(model, "my_first_model_with_shape_info.png", show_shapes=True)
    # x = layers.GlobalAveragePooling1D()(inputs)
    # outputs = layers.Dense(1)(x)
    # model = keras.Model(inputs, outputs)

def CNN(vector_size, num_distances):
    """
    def CNN(num_variants, num_distances):
    model = keras.models.Sequential()
    model.add(Conv1D(1, kernel_size=num_variants, input_shape=(num_distances, 1)))
    model.summary()
    """
    # model = keras.models.Sequential
    inputs = keras.Input(shape=(vector_size,))
    model = inputs
    model = model.add(Conv1D(1, kernel_size=vector_size, input_shape=(num_distances, 1)))
    model = model.add(Conv1D(1, kernel_size=vector_size, input_shape=(num_distances, 1)))
    model = model.add(Conv1D(1, kernel_size=vector_size, input_shape=(num_distances, 1)))
    model = tf.keras.layers.GlobalAveragePooling2D()(x)
    return model# tf.keras.Model(inputs=inputs, outputs=inputs)

    # model.build()
    # model.compile()
    # model.summary()

    # x = inputs
    # x = tf.keras.layers.Conv1D(1, kernel_size=vector_size, input_shape=(5000, 1))(x)
    # x = tf.keras.layers.BatchNormalization()(x)
    # x = tf.keras.layers.GlobalAveragePooling2D()(x)


    # """
    # Construct and return an (uncompiled) conv2d model out of Conv2DBlocks.
    # """
    # inp = tf.keras.Input(shape=(None, None, 3))
    # x = inp
    # x = tf.keras.layers.Conv2D(
    #     filters=32, kernel_size=(7, 7), strides=(1, 1),
    #     dilation_rate=(2, 2), padding='valid')(x)
    # x = tf.keras.layers.BatchNormalization()(x)
    # # x = tf.keras.layers.LeakyReLU()(x)
    # x = tfa.layers.GeLU()(x)
    # x = tf.keras.layers.MaxPool2D(pool_size=(2, 2), strides=(2, 2))(x)
    #
    # for i in range(4):
    #     x = Conv2DBlock(
    #         n_channels=32*(i+1), n_layers=1, kernel_size=(1, 1))(x)
    #     x = ResidualBlock(
    #         n_channels=32*(i+1), n_layers=3, kernel_size=(3, 3))(x)
    #     x = ResidualBlock(
    #         n_channels=32*(i+1), n_layers=3, kernel_size=(3, 3))(x)
    #     x = ResidualBlock(
    #         n_channels=32*(i+1), n_layers=3, kernel_size=(3, 3))(x)
    #     x = tf.keras.layers.MaxPool2D(pool_size=(2, 2), strides=(2, 2))(x)
    #
    # x = tf.keras.layers.GlobalAveragePooling2D()(x)
    # x = tf.keras.layers.Dense(1024)(x)
    # # x = tf.keras.layers.LeakyReLU()(x)
    # x = tfa.layers.GeLU()(x)
    # x = tf.keras.layers.Dropout(0.5)(x)
    #
    # x = tf.keras.layers.Dense(num_classes)(x)
    # out = tf.keras.layers.Softmax()(x)
    # return tf.keras.Model(inputs=inp, outputs=out)