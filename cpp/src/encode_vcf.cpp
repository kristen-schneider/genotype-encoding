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
		int num_samples = bcf_hdr_nsamples(vcf_header);
		cout << "NUM SAMPLES: " << num_samples << endl;
		
		int *nseq;
			
		const char** sequence_names = bcf_hdr_seqnames(vcf_header, nseq);
		cout << sequence_names[0] << endl;
		cout << sequence_names[2548] << endl;
		//cout << nseq[0]<< endl;
		//cout << nseq[2548] << endl;
		cout << "PRINTING" << endl;

		//for (int i = 0; i < 10; i++){
		//	cout << sequence_names[i] << endl;
		//}
	}
	
}
