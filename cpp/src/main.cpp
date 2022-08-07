#include <iostream>
#include <fstream>
#include <map>


#include "encode_vcf.h"
#include "map_encodings.h"
#include "read_config.h"
#include "slice_vcf.h"

using namespace std;

int main(int argc, char* argv[]){
		
	// read config file
	cout << "Reading Config File..." << endl;
	string configFile = argv[1];   // configuration file will all options
	map<string, string> config_options;
	config_options = get_config_options(configFile);
	
	// access each option by variable name
	string encoding_file = config_options["encoding_file"];
	string vcf_file = config_options["vcf_file"];
	int segment_size = stoi(config_options["segment_size"]);
	string out_dir = config_options["out_dir"];
	
	// make encoding map
	map<string, int> encoding_map = make_encoding_map(encoding_file);
	
	// out_file_names
	string vcf_out_file = out_dir + "chr14.segment." + config_options["segment_size"] + ".vcf";
	string encoding_out_file = out_dir + "chr14.segment." + config_options["segment_size"] + ".encoding";

	// slice vcf into segments
	cout << "Slicing VCF..." << endl;
	get_vcf_header(vcf_file, vcf_out_file);
	slice(vcf_file, segment_size, vcf_out_file);	

	// encoded vcf segments 
	cout << "Encoding VCF..." << endl;
	write_encoded_vcf(vcf_out_file, encoding_map, encoding_out_file);


	return 0;
}
