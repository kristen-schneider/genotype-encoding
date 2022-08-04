#configfile: "config.yaml"

rule all:
	input:
		"data/segments/testsegment"
		
rule segment_vcf_COMPILE:
	input:
		main="cpp/src/main.cpp",
		read_config="cpp/src/read_config.cpp",
		map_encodings="cpp/src/map_encodings.cpp",
		slice_vcf="cpp/src/slice_vcf.cpp",
		include="cpp/include/"

	output:
		bin="cpp/bin/segment"
	message:
		"Compiling segment_vcf"
	shell:
		"g++ {input.main}" \
			" {input.read_config}" \
			" {input.map_encodings}" \
			" {input.slice_vcf}" \
			" -I {input.include}" \
			" -o {output.bin}"
		

rule segment_vcf_RUN:
	input:
		bin="cpp/bin/segment",
		config_file="cpp/config_sample"
	output:
		segment="data/segments/testsegment"
	message: 
		"Executing segment_vcf"
	shell:
		"./{input.bin} {input.config_file}"

