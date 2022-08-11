import sys

samples_file = sys.argv[1]
encoding_file = sys.argv[2]
out_file = sys.argv[3]

def main():
    sampleIDs_list = make_sample_IDs_list(samples_file)
    encodings_list = make_encodings_list(encoding_file)
    empty_pairwise_dict = make_pairwise_dictionary(sampleIDs_list)

    distance_dictionary = fill_dictionary(empty_pairwise_dict, sampleIDs_list, encodings_list, out_file)

def make_sample_IDs_list(samples_file):
    print('making sampleID list...')
    sampleIDs_list = []
    f = open(samples_file, 'r')
    for line in f: sampleIDs_list.append(line.strip())
    f.close()

    return sampleIDs_list


def make_encodings_list(encoding_file):
    print('making encoding list...')
    encodings_list = []

    f = open(encoding_file, 'r')
    for line in f: encodings_list.append(line.strip())
    f.close()

    return encodings_list

def make_pairwise_dictionary(sampleIDs_list):
    print('making empty dictionary...')
    pairwise_dict = dict()

    for s1_i in range(len(sampleIDs_list)):
        sample1_ID = sampleIDs_list[s1_i]
        for s2_i in sampleIDs_list[(s1_i + 1):]:
            sample2_ID = s2_i
            key_pair = (sample1_ID, sample2_ID)
            pairwise_dict[key_pair] = -1
    return pairwise_dict

def fill_dictionary(empty_dictionary, sampleIDs_list, encodings_list, out_file):
    o = open(out_file, 'w')
    o.write('sample1ID\tsample2ID\tIBD1_sites\tIBD1_fraction\n')
    print('computing IBD...')
    for k in empty_dictionary.keys():
        sample1_ID_index = sampleIDs_list.index(k[0])
        sample2_ID_index = sampleIDs_list.index(k[1])

        sample1_encoding = encodings_list[sample1_ID_index]
        sample2_encoding = encodings_list[sample2_ID_index]

        IBD1 = compute_IBD1(sample1_encoding, sample2_encoding)

        empty_dictionary[k] = IBD1

        fractionIBD1 = IBD1 / len(sample1_encoding)

        # write data
        line = k[0] + '\t' + k[1] + '\t' + str(IBD1) + '\t' + str(fractionIBD1) + '\n'
        o.write(line)

    o.close()
    return empty_dictionary


def compute_IBD1(sample1, sample2):

    shared_nonREF_genotypes = 0
    if len(sample1) != len(sample2):
        print('input encoding vectors are of different length.\nexiting.')
        return -1

    for i in range(len(sample1)):
        if (sample1[i] != '0') and (sample2[i] != '0'):
            if sample1[i] == sample2[i]:
                shared_nonREF_genotypes += 1

    return shared_nonREF_genotypes

#def write_target_IBD1(distance_dictionary, out_file):
#
#    print('writing data...')
#    o = open(out_file, 'w')
#
#    for pair in distance_dictionary.keys():
#        s1_ID = pair[0]
#        s2_ID = pair[1]
#        d = distance_dictionary[pair]
#        line = s1_ID + '\t' + s2_ID + '\t' + str(d)
#        o.write(line)



if __name__ == '__main__':
    main()
