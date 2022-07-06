import utils


encoded_genotypes_file = '/home/sdp/genotype-encoding/data/genotypes.txt'

def main():
    utils.count_variants(encoded_genotypes_file)

if __name__ == '__main__':
    main()
