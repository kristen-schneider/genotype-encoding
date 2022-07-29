encoded_file = '../ALL.chr14.encoded'
IBD_file = '../ALL.chr14.genome'
sample_names_file = '../ALL.chr14.samples'
cnn_file = '../CNN.input.test'


def main():
    """
    Takes plink.genome file, encoding file, and sample names and outputs to new format for input to CNN.
    New format:
        sample1 sample2 distance
    """
    sampleID_list = make_sampleID_list(sample_names_file)
    print('sample IDs done...')
    encoding_list = make_encoding_list(encoded_file)
    print('encoding done...')
    ID_encoding_dict = make_ID_encoding_dict(sampleID_list, encoding_list)
    print('dictionary done...')
    write_CNN_input(ID_encoding_dict, IBD_file, cnn_file)
    print('writing done...')



def make_encoding_list(encoded_file):
    """
    Makes a list of encodings
    :param encoded_file: file with a list of encodings (in same order as sample names)
    :return: a list of encodings
    """
    encodings_list = []
    f = open(encoded_file, 'r')
    for line in f:
        encodings_list.append(line.strip())
    f.close()
    return encodings_list

def make_sampleID_list(sample_names_file):
    """
    Makes a list of sample names
    :param sample_names_file: file with a list of sample IDs (in same order as encoding file)
    :return: list of sample names
    """
    sampleID_list = []
    f = open(sample_names_file, 'r')
    for line in f:
        sampleID_list.append(line.strip())
    f.close()
    return sampleID_list

def make_ID_encoding_dict(sample_ID_list, encoding_list):
    """
    :param: list of sample IDs and list of encodings
    :return: dictinoary with key as sample ID
    """
    ID_encoding_dict = dict()

    for i in range(len(sample_ID_list)):
        sampleID = sample_ID_list[i]
        encoding = encoding_list[i]

        ID_encoding_dict[sampleID] = encoding
    return ID_encoding_dict

def write_CNN_input(sample_encoding_dict, IBD_file, CNN_input_file):
    f = open(IBD_file, 'r')
    o = open(CNN_input_file, 'w')
    header = None
    for line in f:
        if header == None:
            header = line
        else:
            A = line.strip().split()
            sample1 = A[1]
            sample1_encoding = sample_encoding_dict[sample1]
            sample2 = A[3]
            sample2_encoding = sample_encoding_dict[sample2]
            distance = float(A[11])

            data_line = sample1_encoding + '\t' \
                        + sample2_encoding + '\t' \
                        + str(distance)

            o.write(data_line)

    f.close()
    o.close()

if __name__ == '__main__':
    main()
