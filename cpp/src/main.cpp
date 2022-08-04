#include <iostream>
#include <map>


//#include "make_encoding_map.h"
#include "read_config.h"

using namespace std;

int main(int argc, char* argv[]){

	string configFile = argv[1];   // configuration file will all options
	map<string, string> config_options;

	config_options = get_config_options(configFile);
	string encoding_file = config_options["encoding_file"];
	string vcf_file = config_options["vcf_file"];

	cout << configFile << endl;
	cout << encoding_file << endl;
	cout << vcf_file << endl;
	

	return 0;
}
