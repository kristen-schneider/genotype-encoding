#include <iostream>
#include <fstream>
#include <map>


//#include "make_encoding_map.h"
#include "read_config.h"

using namespace std;

int main(int argc, char* argv[]){

	string configFile = argv[1];   // configuration file will all options
	map<string, string> config_options;

	config_options = get_config_options(configFile);
	
	// access each option by variable name
	string encoding_file = config_options["encoding_file"];
	string vcf_file = config_options["vcf_file"];
	string segment_size = config_options["segment_size"];
	string out_dir = config_options["out_dir"];
	
	// path to out file
	ofstream out_file_stream;
	out_file_stream.open(out_dir + "testsegment");

	if (!out_file_stream.is_open()){
		cout << "ERROR" << endl;
	}
	

	out_file_stream << "TEST" << endl;
	out_file_stream.close();

	return 0;
}
