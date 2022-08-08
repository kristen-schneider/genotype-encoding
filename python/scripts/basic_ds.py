import tensorflow as tf

def build_dataset_from_file(CNN_input_file):
    """
    Builds a tensorflow dataset object from file with 3 columns:
    sample1, sample2, IBD_distance
    :param CNN_input_file:
    :return: tensorflow dataset object for input to cnn model
    """
    f = open(CNN_input_file, 'r')
    header = f.readline()
    sample1_data = []
    sample2_data = []
    distances_data = []
    c = 0
    for line in f:
        print(c)
        currS1 = []
        currS2 = []
        A = line.strip().split()
        for i in A[0]:
            currS1.append(int(i))
        sample1_data.append(currS1)
        for j in A[1]:
            currS2.append(int(j))
        sample2_data.append(currS1)

        distances_data.append(A[2])
        c+=1

    # each set of input data is its own tensor
    sample1_ds = tf.data.Dataset.from_tensor_slices(sample1_data)
    sample2_ds = tf.data.Dataset.from_tensor_slices(sample2_data)
    distances_ds = tf.data.Dataset.from_tensor_slices(distances_data)

    # map distance values to float
    sample1_ds_float = sample1_ds.map(lambda x: int(x))
    sample2_ds_float = sample2_ds.map(lambda x: int(x))
    distances_ds_float = distances_ds.map(lambda x: float(x))

    # zip 3 tensor items together into one dataset
    full_ds = tf.data.Dataset.zip((sample1_ds_float, sample2_ds_float, distances_ds_float))
    # puts 1 element into a batch
    full_ds_batch = full_ds.batch(2)
    return full_ds_batch
