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
    print('Done.')
    print()

    # build base CNN model
    vector_size = num_variants
    # base_cnn = model.build_base_cnn(vector_size)

    ## can encapsulate in own function
    # sample1_input = tf.keras.Input(name="sample1", shape=vector_size)
    # sample2_input = tf.keras.Input(name="sample2", shape=vector_size)
    #
    # predicted_distances = model.DistanceLayer()(
    #     base_cnn(sample1_input),
    #     base_cnn(sample2_input)
    # )
    # siamese_network = tf.keras.Model(inputs=[sample1_input, sample2_input], outputs=predicted_distances)
    ##
    siamese_network = model.build_siamese_network(vector_size)

    siamese_model = model.SiameseModel(siamese_network)
    siamese_model.compile(optimizer=tf.keras.optimizers.Adam(0.0001))
    siamese_model.fit(ds, epochs=3)

if __name__ == '__main__':
    main()
