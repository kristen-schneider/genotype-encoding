#!/bin/bash


cpp_src_dir="./cpp/src/"
cpp_include_dir="./cpp/include/"
cpp_bin_dir="./cpp/bin/"
config_file="./cpp/config_sample"

source ~/miniconda3/etc/profile.d/conda.sh 
conda activate genotype-encoding

bin=$cpp_bin_dir"segment"

# COMPILE
g++ $cpp_src_dir"main.cpp" \
	$cpp_src_dir"read_config.cpp" \
	-I $cpp_include_dir \
	-o $bin

# RUN
$bin $config_file
