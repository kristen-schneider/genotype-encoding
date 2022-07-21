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
        #data_list = [A[0], A[1], float(A[2])] 
        #data.append(data_list)
        data.append(A)
    dataset = tf.data.Dataset.from_tensor_slices(data)
    return dataset

def build_dataset_file(sample1_file, sample2_file, distance_file):
    dataset = tf.data.TextLineDataset([sample1_file, sample2_file, distance_file])
    return dataset
