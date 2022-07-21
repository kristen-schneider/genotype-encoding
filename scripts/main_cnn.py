import build
import model
import utils


import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Conv1D

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
    dataset = build.build_dataset(CNN_input_file)
    # dataset.map(lambda x: x*2)
    print('Done.')
    print()
    # for element in dataset:
    #     print(element)

    # build model
    vector_size = num_variants
    model.CNN(vector_size)

    #input_shape = (batch, length_vector, channels)
    # can test with this
    #x = tf.random.normal(input_shape)
    #net = get_cnn() # cnn defined here
    #y = net(x)

if __name__ == '__main__':
    main()
