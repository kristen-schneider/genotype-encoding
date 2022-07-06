import random

genotypefile = './simulated_genotypes.txt'
positivefile = './simulated_positives.txt'
negativefile = './simulated_negatives.txt'

num_samples = 50
num_variants = 50
encoding_ints = [0,1,2,3]

def main():
    random_genotypes(genotypefile)
    all_zeros(negativefile)


def random_genotypes(outfile):
    o = open(outfile, 'w')
    for i in range(num_samples):    
        for i in range(num_variants):
            v = random.choice(encoding_ints)
            o.write(str(v))
        o.write('\n')

def all_zeros(outfile):
    o = open(outfile, 'w')
    for i in range(num_samples):
        for i in range(num_variants):
            o.write(str(0))
        o.write('\n')

if __name__ == '__main__': 
    main()
