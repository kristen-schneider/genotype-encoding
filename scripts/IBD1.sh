#!bin/bash


sampleIDs='../../precision-medicine/data/ALL.chr14.samples'
sampleEncodings='../../precision-medicine/data/encoded/new.encoded.txt'
output_file='../data/targetIBD1.txt'

python 'IBD1.py' $sampleIDs $sampleEncodings $output_file
