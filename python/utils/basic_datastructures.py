import sys
from collections import defaultdict

sys.path.insert(1, '~genotype-encoding/python/utils/')
import distance_calculations
#from python.utils import distance_calculations

def get_sample_ID_list(sample_ID_file):
    all_sample_IDs = []
    f = open(sample_ID_file, 'r')
    for line in f:
        ID = line.strip()
        all_sample_IDs.append(ID)
    f.close()

    return all_sample_IDs

def get_encoding_list(sample_encodings_file):
    all_sample_encodings = []
    f = open(sample_encodings_file, 'r')
    for line in f:
        encoding = line.strip()
        encoding_list_ints = [int(i) for i in encoding]
        all_sample_encodings.append(encoding_list_ints)
    f.close()

    return all_sample_encodings

def get_ID_encoding_dict(sample_IDs, sample_encodings_file):
    ID_encoding_dict = dict.fromkeys(sample_IDs)

    ID_i = 0
    f = open(sample_encodings_file, 'r')
    for line in f:
        encoding_i = line.strip()
        ID_encoding_dict[sample_IDs[ID_i]] = encoding_i
        ID_i += 1
    f.close()

    if len(sample_IDs) != len(ID_encoding_dict.keys()):
        print('ERROR: not the same number of sample IDs and encodings.')
    return ID_encoding_dict

def get_query_euclidean_dict(query_ID, ID_encoding_dict):
    query_euclidean_dict = {ID: -1 for ID in ID_encoding_dict.keys()}
    query_encoding = ID_encoding_dict[query_ID]

    for ID in ID_encoding_dict.keys():
        sample_encoding = ID_encoding_dict[ID]
        euclidean_distance = distance_calculations.euclidean_distance(query_encoding, sample_encoding)
        query_euclidean_dict[ID] = euclidean_distance
    return query_euclidean_dict

def get_plink_dict(plink_file):
    plink_dict = defaultdict(dict)

    f = open(plink_file, 'r')
    header = f.readline()
    for line in f:
        l = line.strip().split()
        ID1 = l[1]
        ID2 = l[3]
        plink_distance = float(l[11])
        plink_dict[ID1][ID2] = plink_distance
    f.close()
    return plink_dict


    # query_plink_dict = {ID: -1 for ID in ID_encoding_dict.keys()}
    # query_encoding = ID_encoding_dict[query_ID]
    #
    #
    #
    # for ID in ID_encoding_dict.keys():
    #     sample_encoding = ID_encoding_dict[ID]
    #     euclidean_distance = distance_calculations.euclidean_distance(query_encoding, sample_encoding)
    #     query_plink_dict[ID] = euclidean_distance
    # return query_plink_dict

