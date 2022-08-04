#include <iostream>
#include <fstream>
#include <map>


#include "map_encodings.h"
#include "read_config.h"
#include "slice_vcf.h"

using namespace std;

int main(int argc, char* argv[]){

	string configFile = argv[1];   // configuration file will all options
	map<string, string> config_options;

	// read config file
	config_options = get_config_options(configFile);
	
	// access each option by variable name
	string encoding_file = config_options["encoding_file"];
	string vcf_file = config_options["vcf_file"];
	int segment_size = stoi(config_options["segment_size"]);
	string out_dir = config_options["out_dir"];
	
	// make encoding map
	map<string, int> encoding_map = make_encoding_map(encoding_file);
	
	// slice vcf into segments
	slice(vcf_file, segment_size, out_dir + "testsegment");	

	return 0;
}
