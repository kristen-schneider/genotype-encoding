# Segment and Encode VCF<br>
Edit ./cpp/config_sample to include correct data<br>
Edit Snakefile to include correct paths<br>
`snakemake`<br>
<br>

# run plink on a VCF file<br>
`plink --vcf /path/to/vcf/ --genome`<br>
<br>

# make input to CNN model<br>
`python ./python/scripts/make_CNN_input.py
        /path/to/sampleIDs
        /path/to/encoding_file
        /path/to/plink_IBD_file
        /path/to/ID_CNN_output
        /path/to/encoding_CNN_output`<br>
<br>

# run model
`python ./python/scripts/main_cnn.py
        /path/to/sampleIDs
        /path/to/encoding_file
        /path/to/ID_CNN
        /path/to/encoding_CNN`<br>
