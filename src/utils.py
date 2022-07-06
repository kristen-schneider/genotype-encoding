def count_variants(encoded_genotypes_file):
    f = open(encoded_genotypes_file, 'r')
    line = f.readline().strip()
    num_variants = len(line)
    return num_variants
