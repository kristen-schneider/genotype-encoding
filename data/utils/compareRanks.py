import bisect
import operator
from scipy.stats import kendalltau
from collections import defaultdict

from scipy.stats import ranksums

# >>> rng = np.random.default_rng()
# >>> sample1 = rng.uniform(-1, 1, 200)
# >>> sample2 = rng.uniform(-0.5, 1.5, 300) # a shifted distribution
# >>> ranksums(sample1, sample2)
# RanksumsResult(statistic=-7.887059, pvalue=3.09390448e-15)  # may vary
# >>> ranksums(sample1, sample2, alternative='less')
# RanksumsResult(statistic=-7.750585297581713, pvalue=4.573497606342543e-15) # may vary
# >>> ranksums(sample1, sample2, alternative='greater')
# RanksumsResult(statistic=-7.750585297581713, pvalue=0.9999999999999954) # may vary

IDs = '/Users/kristen/PycharmProjects/genotype-encoding/data/ALL.chr14.samples'
HNSW = '/Users/kristen/PycharmProjects/genotype-encoding/data/FAISS/IndexHNSW.out'
L2 = '/Users/kristen/PycharmProjects/genotype-encoding/data/FAISS/FlatL2.out'
PLINK = '/Users/kristen/PycharmProjects/genotype-encoding/data/ALL.chr14.seg.0.genome'

def main():
    sample_ID_list = make_ID_list(IDs)
    sample_ID_dict = make_ID_index_dict(sample_ID_list)

    L2_rankings = rank_faiss(sample_ID_list, L2)
    HNSW_rankings = rank_faiss(sample_ID_list, HNSW)
    PLINK_rankings = rank_plink(PLINK, sample_ID_list, sample_ID_dict)

    # one_sample = 'HG00096'
    # L2_HNSW = kendalltau(L2_rankings[one_sample][1:80], HNSW_rankings[one_sample][1:80])
    # L2_PLINK = kendalltau(L2_rankings[one_sample][1:80], PLINK_rankings[one_sample][1:80])
    # HNSW_PLINK = kendalltau(HNSW_rankings[one_sample][1:80], PLINK_rankings[one_sample][1:80])
    # print('L2-HNSW kendalltau: ', L2_HNSW)
    # print('L2-PLINK kendalltau: ', L2_PLINK)
    # print('HNSW-PLINK kendalltau: ', HNSW_PLINK)
    # print()


    for s in sample_ID_list:
        one_sample = s
        print('SAMPLE: ', s)
        L2_HNSW = kendalltau(L2_rankings[one_sample][1:80], HNSW_rankings[one_sample][1:80])
        L2_PLINK = kendalltau(L2_rankings[one_sample][1:80], PLINK_rankings[one_sample][1:80])
        HNSW_PLINK = kendalltau(HNSW_rankings[one_sample][1:80], PLINK_rankings[one_sample][1:80])
        print('L2-HNSW kendalltau: ', L2_HNSW)
        print('L2-PLINK kendalltau: ', L2_PLINK)
        print('HNSW-PLINK kendalltau: ', HNSW_PLINK)
        print()

    x = 'debug'

def rank_faiss(sample_ID_list, faiss_file):
    num_samples = len(sample_ID_list)
    faiss_rankings = {sampleID: [] for sampleID in sample_ID_list}
    f = open(faiss_file, 'r')

    value_ranked_indexes = []
    for line in f:
        if "QUERY" in line:
            sampleID = sample_ID_list[int(line.split(':')[1].strip())]
        else:
            if len(value_ranked_indexes) == num_samples:
                faiss_rankings[sampleID] = value_ranked_indexes
                value_ranked_indexes = []
            else:
                l = line.strip().split()
                try:
                    index = int(l[0])
                    value_ranked_indexes.append(index)
                except ValueError:
                    continue
    f.close()
    return faiss_rankings

def rank_plink(plink_file, sample_ID_list, sample_ID_dict):
    '''
    {sampleID1: [sorted indexes],
     sampleID2: [sorted indexes],...}

    '''
    ID_ranks = {ID: [] for ID in sample_ID_list}
    # ID_ranks = defaultdict(dict)
    f = open(plink_file, 'r')
    header = None
    if header == None:
        header = f.readline()
    for line in f:
        l = line.strip().split()
        sample1 = l[1]
        sample1_index = sample_ID_dict[sample1]
        sample2 = l[3]
        sample2_index = sample_ID_dict[sample2]
        distance = float(l[11])

        ID_ranks[sample1].append((distance, sample2_index))
        ID_ranks[sample2].append((distance, sample1_index))
    f.close()

    for ID in ID_ranks.keys():
        ID_ranks[ID] = sort_tuples_by_distance(ID_ranks[ID])
    return ID_ranks

def make_ID_list(IDs_file):
    f = open(IDs_file, 'r')
    sample_IDs_list = [line.strip() for line in f]
    f.close()
    return sample_IDs_list

def make_ID_index_dict(sample_IDs_list):
    sample_IDs_dict = {ID: s for s, ID in enumerate(sample_IDs_list)}
    return sample_IDs_dict

def sort_tuples_by_distance(tuple_list):
    new_list = [x for x, y in
     sorted(enumerate(tuple_list, start=1), key=operator.itemgetter(1))]
    return new_list





if __name__ == '__main__':
    main()