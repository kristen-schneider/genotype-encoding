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
#include <vector>

#include "encode_vcf.h"

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
		// gettting all sequence names
		const char **sequence_names = get_sequence_names(vcf_header);
		
		// initialize and allocate bcf1_t object
        	bcf1_t *vcf_record = bcf_init();
        	if (vcf_record == NULL) {
                	cout << "ERROR: record is empty" << endl;
        	}

		vector<vector<int>> all_genotype_encodings; // vector of vectors
		
		while (bcf_read(vcf_stream, vcf_header, vcf_record)){
			bcf_unpack(vcf_record, BCF_UN_ALL);
			bcf_unpack(vcf_record, BCF_UN_INFO);

			// making variable names for each column
			string chrm = bcf_hdr_id2name(vcf_header, vcf_record->rid);
			int pos = (unsigned long)vcf_record->pos;
			string id = vcf_record->d.id;
			string ref = vcf_record->d.allele[0];
			string alt = vcf_record->d.allele[1];
			double_t qual = vcf_record->qual;

			// make chromosome through quality into one vector of strings
			vector<string> chrm_thru_qual_vector = 
				{chrm, to_string(pos), id, ref, alt, to_string(qual)};
			string s;
			for (const auto &col : chrm_thru_qual_vector) s += "\t" + col;
			string chrm_thru_qual_string;
			chrm_thru_qual_string = chrm_thru_qual_string +
				chrm + "\t" +
				to_string(pos) + "\t" +
				id + "\t" +
				ref + "\t" +
				alt + "\t" +
				to_string(qual) + "\t";

			// reading genotypes
			string s_gt;
			int *gt = NULL;
			int ngt = 0;
			int ngt_arr = 0;

			ngt = bcf_get_genotypes(vcf_header, vcf_record,  &gt, &ngt_arr);
			

			vector<int> record_encoding;
		}	
		

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
