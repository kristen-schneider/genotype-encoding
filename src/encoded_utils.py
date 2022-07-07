def count_variants(encoded_genotypes_file):
    f = open(encoded_genotypes_file, 'r')
    line = f.readline().strip()
    num_variants = len(line)
    return num_variants

def read_encoded_file(encoded_file):
    all_vectors = []
    
    f = open(encoded_file, 'r')
    for line in f:
        single_vector = []
        line_ = line.strip()
        #all_vectors.append(line)
        for i in line_:
            single_vector.append(i)

        all_vectors.append(single_vector)
    
    return all_vectors
