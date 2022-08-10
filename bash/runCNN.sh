#!/bin/bash

scripts_dir="/home/sdp/genotype-encoding/python/scripts/"
#sample_IDs_file="./data/fake_data/fake_IDs"
#sample_encodings_file="./data/fake_data/fake_encodings"
#pairwise_distances="./data/fake_data/fake_CNN"
#ds_out_dir="./data/fake_data/ds_zipped"

sample_IDs_file="../precision-medicine/data/ALL.chr14.sampleIDs"
sample_encodings_file="./data/segments/seg_1000/ALL.chr14.seg.0.encoding"
pairwise_distances="./data/segments/seg_1000/ALL.chr14.seg.0.CNN"
#ds_out_dir="./data/datasets/ALL.chr14.seg.0.ds"


source ~/miniconda3/etc/profile.d/conda.sh 
#conda activate genotype-encoding


python $scripts_dir'main_cnn.py' $sample_IDs_file $sample_encodings_file $pairwise_distances
