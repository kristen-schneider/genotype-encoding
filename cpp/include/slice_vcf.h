#ifndef SLICE_VCF_H
#define SLICE_VCF_H

#endif //SLICE_VCF_H

#include <iostream>
#include <fstream>
#include <string>

using namespace std;

void get_vcf_header(string vcf_file);
void slice(string vcf_file, int segment_size, string out_file);
