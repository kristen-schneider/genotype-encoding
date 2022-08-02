"""
Title: Similarity between two vectors for IBD
Authors: Kristen Schneider
Date created: 2022/07/20
Last modified: 2022/07/20
Description: Inspired by [code](https://keras.io/examples/vision/siamese_network/) written by [Hazem Essam](https://twitter.com/hazemessamm) and [Santiago L. Valdarrama](https://twitter.com/svpino)
"""

import basic_ds
import tfrecord_ds
import model
import utils

import tensorflow as tf

CNN_input_file = '../data/fake_input.txt'
tf_records_dir = '../data/tfrecords/'

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
    # Initialize DataWriter
    DW = tfrecord_ds.DataWriter(CNN_input_file, tf_records_dir)
    # Get basic dataset for whole file (string, string, float)
    # basicDS = tfrecord_ds.DataWriter.get_basic_dataset(CNN_input_file)
    # Serialize dataset and write to tfrecord
    tfrecord_ds.DataWriter.to_tfrecords(DW, basicDS)

    # ds = basic_ds.build_dataset_from_file(CNN_input_file)
    print('Done.')
    print()

    # print('Running...')
    # vector_size = num_variants
    # siamese_network = model.build_siamese_network(vector_size)
    # siamese_model = model.SiameseModel(siamese_network)
    # siamese_model.compile(optimizer=tf.keras.optimizers.Adam(0.0001))
    # siamese_model.fit(ds, epochs=3)

if __name__ == '__main__':
    main()
