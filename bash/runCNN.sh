#!/bin/bash


scripts_dir="./python/scripts/"
sample_IDs_file="../precision-medicine/data/ALL.chr14.sampleIDs"
sample_encodings_file="./data/segments/seg_5000/ALL.chr14.seg.0.encoding"
IDs_distances_file="./data/segments/seg_5000/ALL.chr14.seg.0.CNN_IDs"
encoding_distances_file="./data/segments/seg_5000/ALL.chr14.seg.0.CNN_encodings"
#ds_out_dir="./data/datasets/ALL.chr14.seg.0.ds"


## FAKE DATA
#sample_IDs_file="./data/fake_data/fake_IDs_40x100"
#sample_encodings_file="./data/fake_data/fake_encodings_40x100"
#IDs_distances_file="./data/fake_data/fake_ID_distances_40x100"
#encoding_distances_file="./data/fake_data/fake_encoding_distances_40x100"
#ds_out_dir="./data/fake_data/ds_zipped"

source ~/miniconda3/etc/profile.d/conda.sh 
#conda activate genotype-encoding


python $scripts_dir/main_cnn.py $sample_IDs_file $sample_encodings_file $IDs_distances_file $encoding_distances_file
