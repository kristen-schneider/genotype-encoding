import math
import random
import sys

num_samples = int(sys.argv[1])
num_variants = int(sys.argv[2])
out_file = sys.argv[3]

def main():

    # generate a list of samples
    all_samples = []
    for s in range(num_samples):
        sample_i_encoding = generate_encoding(num_variants)
        all_samples.append(sample_i_encoding)
    
    # write to file
    f = open(out_file, 'w')
    f.write('sample1\tsample2\tdistance\n')
    
    for sample_i in range(num_samples):
        sample1 = all_samples[sample_i]
        
        for sample_j in range(num_samples - sample_i):
            if sample_i == sample_j:
                continue
            else:
                sample2 = all_samples[sample_j]
                distance = compute_distance(sample1, sample2)
                line = sample1 + '\t' + sample2 + '\t' + str(distance) + '\n'
                f.write(line) 

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

def compute_eucliddea_distance(sample1, sample2):
    num_variants = len(sample1)
    ED = 0
    sum_d = 0
    for i in range(len(sample1)):
        d = sample1[i] - sample2[i]
        d_sqrd = math.pow(d, 2)
        sum_d += d_sqrd

    ED = math.sqrt(sum_d)
    return ED

if __name__ == '__main__':
    main()
