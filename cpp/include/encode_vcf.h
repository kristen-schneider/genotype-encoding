#ifndef ENCODEVCF_H
#define ENCODEVCF_H

#endif //ENCODEVCF_H

#include <iostream>
#include <fstream>
#include <map>
#include <string>

using namespace std;

void write_encoded_vcf(string input_vcf_file, map<string, int> encoding_map, string output_encoding_file);
