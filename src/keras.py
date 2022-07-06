import encoded_utils
import tensorflow as tf
from tensorflow.keras.applications import resnet


encoded_genotype_file = '/home/sdp/genotype-encoding/data/genotype.txt'
encoded_positive_file = '/home/sdp/genotype-encoding/data/positive.txt'
encoded_negative_file = '/home/sdp/genotype-encoding/data/negative.txt'

def main():
    # counting variants for dimension of vector
    num_variants = encoded_utils.count_variants(encoded_genotype_file)
    
    # loading vectors (anchor, positive, and negative)
    genotype_vectors = encoded_utils.read_encoded_file(encoded_genotype_file)
    positive_vectors = encoded_utils.read_encoded_file(encoded_positive_file)
    negative_vectors = encoded_utils.read_encoded_file(encoded_negative_file)

    # counting samples for dimension of dataset
    num_samples = len(genotype_vectors)
    print(type(num_samples), num_samples)
    print(num_variants, num_samples)
    target_shape = (num_variants,)

    # making dataset objects from lists
    genotype_dataset = tf.data.Dataset.from_tensor_slices(genotype_vectors)
    positive_dataset = tf.data.Dataset.from_tensor_slices(positive_vectors)
    negative_dataset = tf.data.Dataset.from_tensor_slices(positive_vectors)


    #DEBUG
    print('Genotype vectors\n')
    for i in genotype_dataset: print(i)
    #for i in positive_dataset: print(i)
    #for i in negative_dataset: print(i)

    dataset = tf.data.Dataset.zip((genotype_dataset, positive_dataset, negative_dataset))
    #dataset = dataset.shuffle(buffer_size=1024)
    #dataset = dataset.map(genotype_dataset, positive_dataset, negative_dataset)

    # split dataseet into train and validation
    train_dataset = dataset.take(round(num_samples * 0.8))
    val_dataset = dataset.skip(round(num_samples * 0.8))

    train_dataset = train_dataset.batch(32, drop_remainder=False)
    train_dataset = train_dataset.prefetch(tf.data.AUTOTUNE)

    val_dataset = val_dataset.batch(32, drop_remainder=False)
    val_dataset = val_dataset.prefetch(tf.data.AUTOTUNE)

    # generate embeddings
    base_cnn = resnet.ResNet50(
        weights='imagenet', input_shape=target_shape + (3,), include_top=False
    )
    
    #flatten = layers.Flatten()
    



if __name__ == '__main__':
    main()
