#include <iostream>
#include <fstream>
#include <string>

using namespace std;

void get_vcf_header(string vcf_file, string out_file){
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
                while(getline(vcf_file_stream, line)){
			char char1 = line.at(0);
			if( char1 == '#'){
				out_file_stream << line << endl;
			}
                }
        }
}

void slice(string vcf_file, int segment_size, string out_file){

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

		// open out file
		ofstream out_file_stream;
		out_file_stream.open(out_file);
		// read vcf file 
		while(getline(vcf_file_stream, line)){
			line_count += 1;
		}
	}
}
