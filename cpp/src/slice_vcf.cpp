#include <iostream>
#include <fstream>
#include <string>

#include "slice_vcf.h"

using namespace std;

void get_vcf_header(string vcf_file, string out_file){
	/*
	 * open VCF file and write header data to out_file
	 */
	 
	// open file and check success
        ifstream vcf_file_stream;
        vcf_file_stream.open(vcf_file);
        if (!vcf_file_stream.is_open()){
                cout << "FAILED TO OPEN: " << vcf_file << endl;
        }
        // read file
        else{
		// open out file
		ofstream out_file_stream;
		out_file_stream.open(out_file);
                
		string line;
                // read vcf file 
                while (getline (vcf_file_stream, line)){
			char char1 = line.at(0);
			if (char1 == '#'){
				out_file_stream << line << endl;
			}
                }
        }
}

void slice(string vcf_file, int segment_size, string out_file){
	/*
	 * Open VCF file, ignore header,
	 * write a segment of columns to out_file
	 */
		
	// open file and check success
        ifstream vcf_file_stream;
        vcf_file_stream.open(vcf_file);
        if (!vcf_file_stream.is_open()){
                cout << "FAILED TO OPEN: " << vcf_file << endl;
        }
        // read file
        else{
		string line;
		int line_count = 0;

		// open out file in append mode
		ofstream out_file_stream;
		out_file_stream.open(out_file, ios_base::app);

		// read vcf file until segment length up
		while (line_count < segment_size){
			getline (vcf_file_stream, line);
			// ingore header
			if (line.at(0) != '#'){
				out_file_stream << line << endl;
				line_count ++;
			}
		}
		cout << "SEGMENT LENGTH: " << segment_size << endl;
		cout << "LINE COUNT: " <<line_count << endl;
	}
}
