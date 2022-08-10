import sys

sample_IDs_file = sys.argv[1]
sample_encodings_file = sys.argv[2]
plink_IBD_file = sys.argv[3]
CNN_input_file = sys.argv[4]

def main():
    ID_list = sample_IDs_list(sample_IDs_file)
    ID_encoding_dictionary = ID_encoding_dict(ID_list, sample_encodings_file)
    write_CNN_input(ID_encoding_dictionary, plink_IBD_file, CNN_input_file)

def sample_IDs_list(sample_IDs_file):
    ID_list = []
    
    ID_f = open(sample_IDs_file, 'r')
    for line in ID_f:
        ID_list.append(line.strip())

    ID_f.close()
    
    return ID_list

def ID_encoding_dict(ID_list, sample_encodings_file):
    
    ID_i = 0
    ID_encoding_dictionary = dict()
    encodings_f = open(sample_encodings_file, 'r')
   
    for line in encodings_f:
        encoding = line.strip()
        ID_encoding_dictionary[ID_list[ID_i]] = encoding
        ID_i += 1
    
    encodings_f.close()

    return ID_encoding_dictionary

def write_CNN_input(ID_encoding_dictionary, plink_IBD_file, CNN_input_file):

    plink_f = open(plink_IBD_file, 'r')
    CNN_f = open(CNN_input_file, 'w')

    header = 'encoding1\tencoding\tdistances\n'
    CNN_f.write(header)

    header = None
    for line in plink_f:
        if (header == None):
            header = line
        else:
            A = line.strip().split()
            ID1 = A[1]
            ID2 = A[3]
            distance = float(A[11])

            ID1_encoding = ID_encoding_dictionary[ID1]
            ID2_encoding = ID_encoding_dictionary[ID2]
        

            pairwise_entry = ID1_encoding + '\t' + ID2_encoding + '\t' + str(distance) + '\n'
            CNN_f.write(pairwise_entry)

    plink_f.close()
    CNN_f.close()


if __name__ == '__main__':
    main()
