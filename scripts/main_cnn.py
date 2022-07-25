import dataset
import model
import utils


import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Conv1D

CNN_input_file = '../data/fake_input.txt'
sample1_file = '../data/fake_sample1.txt'
sample2_file = '../data/fake_sample2.txt'
distances_file = '../data/fake_distances.txt'

class DistanceLayer(tf.keras.layers.Layer):
    """
    Computes distance between two vectors with simple euclidean distance
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def call(self, sample1, sample2):
        distance = tf.reduce_sum(tf.norm(sample1 - sample2, ord='euclidean'))
        return distance

def main():

    # find dimensions of incoming data
    #   number of variants = size of input vector
    #   number of distances = number of pairwise distances computed
    [num_variants, num_distances] = utils.CNN_input_dimensions(CNN_input_file)
    print('Opened file: ', CNN_input_file)
    print('...Number of Variants: ', num_variants)
    print('...Number of Pairwise Distances: ', num_distances)
    print()
    
    # dataloader
    #   tf.Dataset works from memory arrays
    #   tfrecord binary format reads from file
    print('Building dataset...')
    ds = dataset.build_dataset_from_file(CNN_input_file)
    # for d in dataset: print(d)
    # for s1, s2, d in dataset:
    #     print(s1)
    #     print(s1.shape)
    print('Done.')
    print()

    # build base CNN model
    vector_size = num_variants
    base_cnn = model.base_cnn(vector_size)
    base_cnn.summary()

    # get embedding for a vector from model
    embedding = tf.keras.Model(base_cnn.input, base_cnn.output, name="embedding")

    # sample 1 and 2 inputs
    sample1_input = tf.keras.layers.Input(name="sample1", shape=vector_size)
    sample2_input = tf.keras.layers.Input(name="sample2", shape=vector_size)

    distances = DistanceLayer()(
        embedding(sample1_input),
        embedding(sample2_input)
    )

    # input_shape = (batch, length_vector, channels)
    # can test with this
    # x = tf.random.normal(input_shape)
    # net = get_cnn() # cnn defined here
    # y = net(x)

if __name__ == '__main__':
    main()
