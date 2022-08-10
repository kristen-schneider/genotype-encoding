import math
import random
import sys

num_samples = int(sys.argv[1])
num_variants = int(sys.argv[2])
sample_ID_file = sys.argv[3]
sample_encoding_file = sys.argv[4]
ID_distance_file = sys.argv[5]
encoding_distance_file = sys.argv[6]

def main():

    # write sample IDs to file
    print('writing sample id file')
    id_file = open(sample_ID_file, 'w')
    all_IDs = generate_sample_IDs(num_samples)
    for i in all_IDs:
        id_file.write(i)
        id_file.write('\n')


    # write sample encodings to file
    print('writing sample encodings file')
    e_file = open(sample_encoding_file, 'w')
    all_encodings = []
    for s in range(num_samples):
        sample_i_encoding = generate_encoding(num_variants)
        e_file.write(sample_i_encoding)
        e_file.write('\n')
        all_encodings.append(sample_i_encoding)

    # write pairwise distances to file
    print('writing pairwise distances to file')
    IDOUT_file = open(ID_distance_file, 'w')
    IDOUT_file.write('sample1_ID\tsample2_ID\tdistance\n')
    
    eOUT_file = open(encoding_distance_file, 'w')
    eOUT_file.write('sample1_encoding\tsample2_encoding\tdistance\n')



    for sample_i in range(num_samples):
        samplei_ID = all_IDs[sample_i]
        samplei_encoding = all_encodings[sample_i]
        for sample_j in range(num_samples):
            if sample_i >= sample_j:
                continue
            else:
                samplej_ID = all_IDs[sample_j]
                samplej_encoding = all_encodings[sample_j]
                distance = compute_euclidean_distance(samplei_encoding, samplej_encoding)
             
                ID_distance_data = samplei_ID + '\t' \
                                + samplej_ID + '\t' \
                                + str(distance) + '\n'
                IDOUT_file.write(ID_distance_data)

                encoding_distance_data = samplei_encoding + '\t' \
                                + samplej_encoding + '\t' \
                                + str(distance) + '\n'
                eOUT_file.write(encoding_distance_data)

    id_file.close()
    e_file.close()
    IDOUT_file.close()
    eOUT_file.close()

def generate_sample_IDs(num_samples):
    sample_IDs = []
    base_name = 'sample'
    for i in range(num_samples):
        sampleID = base_name + str(i)
        sample_IDs.append(sampleID)
    return sample_IDs


def generate_encoding(num_variants):
    options = [0, 1, 2, 3]
    encoding_string  = ''
    
    encoding_list = random.choices(options, weights=(10, 3, 1, 1), k=num_variants)
    for e in encoding_list:
        encoding_string += str(e)
    
    return encoding_string



def compute_distance(sample1, sample2):
    num_variants = len(sample1)
    similarity = 0
    for i in range(len(sample1)):
        if sample1[i] == sample2[i]:
            similarity += 1
        else:
            continue
    distance = similarity/num_variants
    return distance

def compute_euclidean_distance(sample1, sample2):
    num_variants = len(sample1)
    ED = 0
    sum_d = 0
    for i in range(len(sample1)):
        d = int(sample1[i]) - int(sample2[i])
        d_sqrd = math.pow(d, 2)
        sum_d += d_sqrd

    ED = math.sqrt(sum_d)
    return ED

if __name__ == '__main__':
    main()
