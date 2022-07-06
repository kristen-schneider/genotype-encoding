import encoded_utils
import tensorflow as tf


encoded_genotype_file = '/home/sdp/genotype-encoding/data/genotype.txt'
encoded_positive_file = '/home/sdp/genotype-encoding/data/positive.txt'
encoded_negative_file = '/home/sdp/genotype-encoding/data/negative.txt'

def main():
    # counting variants for dimension of vector
    num_variants = encoded_utils.count_variants(encoded_genotype_file)
    target_shape = (1, num_variants)
    
    # loading vectors (anchor, positive, and negative)
    genotype_vectors = encoded_utils.read_encoded_file(encoded_genotype_file)
    positive_vectors = encoded_utils.read_encoded_file(encoded_positive_file)
    negative_vectors = encoded_utils.read_encoded_file(encoded_negative_file)

    # counting samples for dimension of dataset
    num_samples = len(genotype_vectors)
    print(num_variants, num_samples)



    dataset = tf.data.Dataset.zip((genotype_vectors, positive_vectors, negative_vectors))
    #dataset = dataset.shuffle(buffer_size=1024)
    #dataset = dataset.map(preprocess_triplets)

if __name__ == '__main__':
    main()
