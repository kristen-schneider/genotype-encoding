#include <iostream>
#include <fstream>
#include <math.h>
#include <map>
#include <string>
#include <htslib/hts.h>
#include <htslib/vcf.h>
#include <htslib/vcfutils.h>
#include <htslib/kstring.h>
#include <htslib/kseq.h>
#include <htslib/synced_bcf_reader.h>

using namespace std;

void write_encoded_vcf(string input_vcf_file, map<string, int> encoding_map, string output_encoding_file){
	/*
	 * Takes a segmented input vcf file, and a mapped encoding
	 * and writes out to a new, encoded file
	 */

	// convert file string to const char
	const char *vcfFile = input_vcf_file.c_str();

	// open output file to write encoding
	ofstream output_stream;
	output_stream.open(output_encoding_file);

	// open VCF file with htslib
	htsFile *vcf_stream = bcf_open(vcfFile, "r");
	if (!vcf_stream){
		cout << "FAILED TO OPEN: " << input_vcf_file << endl;
	}
	else{
		// bcf_hdr_t: 3 dictionaries. https://github.com/samtools/htslib/blob/develop/htslib/vcf.h
		//	1. IDs: "FILTER/INFO/FORMAT" lines
		//	2. Sequence names and lengths in "contig" lines
		//	3. Sample names. 
		bcf_hdr_t *vcf_header = bcf_hdr_read(vcf_stream);
		if (vcf_header == NULL) {
                	throw runtime_error("Unable to read header.");
        	}
		
		// getting number of samples
		int num_samples = get_num_samples(vcf_header);
		cout << "NUM SAMPLES: " << num_samples << endl;
		const char **sequence_names = get_sequence_names(vcf_header);


	}
	
}

int get_num_samples(bcf_hdr_t *vcf_header){
	/*
	 * returns number of samples in VCF file
	 */

	int num_samples = -1;
	num_samples = bcf_hdr_nsamples(vcf_header);
	return num_samples;
}

const char **get_sequence_names(bcf_hdr_t *vcf_header){
	/*
	 * returns sequnce IDs/names in VCF file
	 */
	int n = 0;
	
	const char **sequence_names = NULL;
	bcf_hdr_seqnames(vcf_header, &n);
	
	return sequence_names;
}
