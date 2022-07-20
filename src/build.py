import tensorflow as tf

'''
reads input file and builds dataset
'''
def build_dataset(CNN_input_file):
    
    f = open(CNN_input_file, 'r')
    header = f.readline()
    data = []
    for line in f:
        A = line.strip().split()
        data.append(A)

    dataset = tf.data.Dataset.from_tensor_slices(data)
    return dataset
