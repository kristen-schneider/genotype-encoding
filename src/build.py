import tensorflow as tf

def build_dataset(CNN_input_file):
    """
    reads input file and builds dataset
    """
    # open file and read 3 columns into three tensorflow objects
    f = open(CNN_input_file, 'r')
    header = f.readline()
    sample1_data = []
    sample2_data = []
    distances_data = []
    for line in f:
        A = line.strip().split()
        sample1_data.append(A[0])
        sample2_data.append(A[1])
        distances_data.append(A[2])

    # each set of input data is its own tensor
    sample1_ds = tf.data.Dataset.from_tensor_slices(sample1_data)
    sample2_ds = tf.data.Dataset.from_tensor_slices(sample2_data)
    distances_ds = tf.data.Dataset.from_tensor_slices(distances_data)
    # map distance values to float
    distances_ds_float = distances_ds.map(lambda x: float(x))

    # zip 3 tensor items together into one dataset
    full_ds = tf.data.Dataset.zip((sample1_ds, sample2_ds, distances_ds_float))

    return full_ds
