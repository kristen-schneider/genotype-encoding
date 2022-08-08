"""
Title: Similarity between two vectors for IBD
Authors: Kristen Schneider
Date created: 2022/07/20
Last modified: 2022/07/20
Description: Inspired by [code](https://keras.io/examples/vision/siamese_network/) written by [Hazem Essam](https://twitter.com/hazemessamm) and [Santiago L. Valdarrama](https://twitter.com/svpino)
"""

import basic_ds
import model
import sys
import tfrecord_ds
import utils

import tensorflow as tf

#CNN_input_file = '../data/fake_input.txt'
#sampleIDs_file = '../data/ALL.chr14.samples'
#sampleEncoding_file = '../data/ALL.chr14.encoded'
#pairwiseIBD_file = '../data/ALL.chr14.genome'
#tf_records_dir = '../data/tfrecords/'

#sampleIDs_file = sys.argv[1]
#sampleEncoding_file = sys.argv[2]
#plinkIBD_file = sys.argv[3]
CNN_input_file = sys.argv[1]
ds_output_file = sys.argv[2]
#tf_records_dir = sys.argv[4]

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
    #DW = tfrecord_ds.DataWriter(sampleIDs_file, sampleEncoding_file, pairwiseIBD_file, tf_records_dir)
    #DW.to_tfrecords()
    # Get basic dataset for whole file (string, string, float)
    # basicDS = tfrecord_ds.DataWriter.get_basic_dataset(CNN_input_file)
    # Serialize dataset and write to tfrecord
    # tfrecord_ds.DataWriter.to_tfrecords(DW, W)

    #ds = basic_ds.build_dataset_from_file(CNN_input_file)
    #print('Writing dataset to zip file...')
    #tf.data.experimental.save(
    #    ds, ds_output_file, compression='GZIP'
    #)

    # load dataset from file
    ds = tf.data.experimental.load(
        ds_output_file, element_spec=None, compression='GZIP', reader_func=None
    )
    print('Done.')
    print()

    print('Running...')
    # getting size of the input encoding vectors
    vector_size = num_variants

    # building network
    siamese_network = model.build_siamese_network(vector_size)

    # building model
    siamese_model = model.SiameseModel(siamese_network)
    siamese_model.compile(optimizer=tf.keras.optimizers.Adam(0.0001))

    # training model
    siamese_model.fit(ds, epochs=10)

if __name__ == '__main__':
    main()
