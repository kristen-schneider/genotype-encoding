#!/bin/bash


scripts_dir="./python/scripts/"
sample_IDs_file="../precision-medicine/data/ALL.chr14.sampleIDs"
sample_encodings_file="./data/segments/ALL.chr14.seg.0.encoding"
pairwise_distances="./data/segments/ALL.chr14.seg.0.CNN"
ds_out_dir="./data/datasets/ALL.chr14.seg.0.ds"

#sample_IDs_file="./data/fake_data/fake_IDs_40x100"
#sample_encodings_file="./data/fake_data/fake_encodings_40x100"
#pairwise_distances="./data/fake_data/fake_pairwise_distances_40x100"
#ds_out_dir="./data/fake_data/ds_zipped"

source ~/miniconda3/etc/profile.d/conda.sh 
#conda activate genotype-encoding


python $scripts_dir/main_cnn.py $sample_IDs_file $sample_encodings_file $pairwise_distances $ds_out_dir
