import utils

from tensorflow import keras
from tensorflow.keras.layers import Conv1D

CNN_input_file = '/Users/kristen/PycharmProjects/genotype-encoding/data/CNN.input.txt'

def main():
    # find dimensions of incoming data
    #   number of variants = size of input vector
    #   number of samples = number of vectors
    [num_variants, num_samples] = CNN_input_dimensions(CNN_input_file)

    # dataloader
#    CNN(int(num_variants), int(num_samples))
#
#def CNN(num_variants, num_samples):
#    model = keras.models.Sequential()
#    model.add(Conv1D(1, kernel_size=num_variants, input_shape=(num_samples, 1)))
#    model.summary()
#
#if __name__ == '__main__':
#    main()
