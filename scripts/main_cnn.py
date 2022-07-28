"""
Title: Similarity between two vectors for IBD
Authors: Kristen Schneider
Date created: 2022/07/20
Last modified: 2022/07/20
Description: Inspired by [code](https://keras.io/examples/vision/siamese_network/) written by [Hazem Essam](https://twitter.com/hazemessamm) and [Santiago L. Valdarrama](https://twitter.com/svpino)
"""

import dataset
import model
import utils

import tensorflow as tf
from tensorflow import keras

CNN_input_file = '../data/fake_input.txt'
sample1_file = '../data/fake_sample1.txt'
sample2_file = '../data/fake_sample2.txt'
distances_file = '../data/fake_distances.txt'

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
    # for d in ds: print(d)
    # for s1, s2, d in ds:
    #     print(s1)
    #     print(s1.shape)
    print('Done.')
    print()

    # print('Retrieving target distances...')
    # target_distances = dataset.target_distances(CNN_input_file)
    # print('Done.')

    # build base CNN model
    vector_size = num_variants
    base_cnn = model.base_cnn(vector_size)
    # base_cnn.summary()

    # get embedding for a vector from model
    # baseCNN = tf.keras.Model(base_cnn.input, base_cnn.output, name="embedding")

    # # sample 1 and 2 inputs

    # for s1, s2, td in ds:
    #     sample1_input = s1
    #     sample2_input = s2
    #     target_distance_input = td

    # sample1_input = base_cnn
    ## can encapsulate in own function
    sample1_input = tf.keras.Input(name="sample1", shape=vector_size)
    sample2_input = tf.keras.Input(name="sample2", shape=vector_size)

    predicted_distances = model.DistanceLayer()(
        base_cnn(sample1_input),
        base_cnn(sample2_input)
    )
    siamese_network = tf.keras.Model(inputs=[sample1_input, sample2_input], outputs=predicted_distances)
    ##

    siamese_model = model.SiameseModel(siamese_network)
    siamese_model.compile(optimizer=tf.keras.optimizers.Adam(0.0001))
    siamese_model.fit(ds, epochs=10)

    # input_shape = (batch, length_vector, channels)
    # can test with this
    # x = tf.random.normal(input_shape)
    # net = get_cnn() # cnn defined here
    # y = net(x)

if __name__ == '__main__':
    main()
