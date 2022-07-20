import utils
import build

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Conv1D

CNN_input_file = '../data/fake_input.txt'

def main():

    # find dimensions of incoming data
    #   number of variants = size of input vector
    #   number of distances = number of pairwise distances computed
    [num_variants, num_distances] = utils.CNN_input_dimensions(CNN_input_file)
    print('Opened file: ', CNN_input_file)
    print('...Number of Variants: ', num_variants)
    print('...Number of Pairwise Distances: ', num_distances)

    # dataloader
    #   tf.Dataset works from memory arrays
    #   tfrecord binary format reads from file
    dataset = build.build_dataset(CNN_input_file)
    for element in dataset:
        print(element)    

#def build_dataset(CNN_input_file):
#    f = open(CNN_input_file, 'r')
#    data = []
#    for line in f:
#        A = line.strip().split()
#        data.append(A)
#    
#    dataset = tf.data.Dataset.from_tensor_slices(data)
#    return dataset


#    CNN(int(num_variants), int(num_distances))
#
#def CNN(num_variants, num_distances):
#    model = keras.models.Sequential()
#    model.add(Conv1D(1, kernel_size=num_variants, input_shape=(num_distances, 1)))
#    model.summary()
#
if __name__ == '__main__':
    main()
